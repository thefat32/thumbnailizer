import os
import json
import uuid
import shutil
import soffice_convert


class FileNotFoundError(Exception):
    pass


class InvalidDirectoryError(Exception):
    pass


class UnsupportedOutputFormatError(Exception):
    pass


class UnsupportedInputFormatError(Exception):
    pass


DEFAULT_OPTIONS = {
    'type': 'thumbnail',
    'width': 300,
    'height': 300,
    'quality': 85,
    'trim': False,
    'multi': False,
    'multi_size_max': 5
}


def generate_thumbnail(input, output_dir, output_format, options=None):

    if not os.path.isfile(input):
        raise FileNotFoundError("Invalid input file")

    if not os.path.isdir(output_dir):
        raise InvalidDirectoryError("Invalid Output Dir")

    if options is None:
        options = DEFAULT_OPTIONS.copy()
    else:
        merge_options = DEFAULT_OPTIONS.copy()
        merge_options.update(options)
        options = merge_options

    input_file_without_ext = os.path.splitext(os.path.basename(input))[0]
    input_ext = os.path.splitext(input)[1].replace('.', '')
    output_ext = output_format
    output = f'{output_dir}/{input_file_without_ext}{"-%03d" if options["multi"] else ""}.{output_format}'

    imgcommand = f'convert {"-trim" if options["trim"] else ""} -quality {options["quality"]} -geometry {options["height"]} -extent {options["width"]}X{options["height"]} -colorspace RGB %s %s'

    vidcommand = f'ffmpeg -y -i %s -vf "select=\'eq(pict_type,PICT_TYPE_I)\',scale=300:300:force_original_aspect_ratio=decrease,pad=300:300:(ow-iw)/2:(oh-ih)/2" -fps_mode vfr -frames:v {options["multi_size_max"] if options["multi"] else 1} %s'

    if output_ext not in ['png', 'jpg', 'gif']:
        raise UnsupportedOutputFormatError(
            f'Output extension {output_ext} is not supported.'
        )

    mimedb_path = os.path.dirname(os.path.realpath(__file__)) + '/mimedb.json'
    with open(mimedb_path) as json_file:
        mimedb = json.load(json_file)

    filetype = None
    for mime_type_name in mimedb:
        mime_type = mimedb[mime_type_name]
        if 'extensions' in mime_type:
            for extension in mime_type['extensions']:
                if extension == input_ext:
                    if mime_type_name.split('/')[0] == 'image':
                        filetype = 'image'
                    elif mime_type_name.split('/')[0] == 'video':
                        filetype = 'video'
                    else:
                        filetype = 'other'
                    break
        if filetype is not None:
            break
    else:
        raise UnsupportedInputFormatError(
            f'Input file extendion {input_ext} is not supported.'
        )

    if filetype == 'video':
        command = vidcommand % (input, output)
        os.system(command)
    elif filetype == 'image':
        command = imgcommand % (input, output)
        os.system(command)
    elif filetype == 'other':
        random_uuid = uuid.uuid4()
        tmp_folder = f'/tmp/{random_uuid}'
        soffice_convert.convert_file(
            input,
            tmp_folder,
            'png',
            5)
        command = imgcommand % (
            f"{tmp_folder}/{input_file_without_ext}.png",
            output
        )
        os.system(command)
        shutil.rmtree(tmp_folder)

    return True
