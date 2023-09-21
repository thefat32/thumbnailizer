import logging
import os
import subprocess

logger = logging.getLogger()
logger.setLevel(logging.INFO)

LIBREOFFICE_PATH = os.environ['LIBREOFFICE_PATH']


class ConversionError(Exception):
    pass


def convert_file(
    filepath: str,
    outdir: str,
    convert_to: str,
    num_attempts: int,
) -> None:
    """
    Calls LibreOffice to convert `filepath` to the output type specified in 
    `convert_to`

    :param filepath: the path to the input file
    :param outdir: the path to the output directory
    :param convert_to: the file format of the converted type
    :param num_attempts: number of conversion attempts to make
    :raise ConversionError: if the conversion cannot be performed
    """
    commands = [
        LIBREOFFICE_PATH,
        '--headless',
        '--invisible',
        '--nodefault',
        '--nofirststartwizard',
        '--nolockcheck',
        '--nologo',
        '--norestore',
        '--writer',
        '--convert-to',
        convert_to,
        '--outdir',
        outdir,
        filepath
    ]

    filepath_name_without_ext = os.path.splitext(os.path.basename(filepath))[0]
    expected_outpath = f'{outdir}/{filepath_name_without_ext}.{convert_to.split(":")[0]}'

    # On a cold start, LibreOffice often requires several attempts to convert
    # a file before it succeeds
    print(commands)
    for attempt in range(num_attempts):
        response = subprocess.run(commands)

        if response.returncode == 0 and os.path.exists(expected_outpath):
            logger.info(
                f'Conversion successful on attempt {attempt+1}/{num_attempts}.'
            )
            break

        logger.info(
            f'Conversion attempt {attempt+1}/{num_attempts} failed.'
        )
    else:
        raise ConversionError(
            f'Unable to convert file on {num_attempts} attempts'
            f'Command: {" ".join(commands)}'
        )
