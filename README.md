# Thumbnailizer

An AWS lambda function to generate thumbnails for every known file

## Init Project

### Create a virtualenv (Python 3)

- MacOS and Linux:

  ```
  python3 -m venv .venv
  ```

- Windows
  ```
  python -m venv .venv
  ```

### Activate your virtualenv

- Linux / MacOS
  ```
  source .venv/bin/activate
  ```
- PowerShell
  ```
  .venv\Scripts\Activate.ps1
  ```

### Install the required dependencies.

```
pip install -r requirements.txt
```

### Init CDK

```
cdk bootstrap aws://ACCOUNT-NUMBER/REGION --profile xxx
```

### Deploy:

```
cdk deploy --all
```

## Debug using SAM in VSCode

### CDK Synth

```
cdk synth --all --quiet --profile profile-name
```

### SAM build

```
sam build -t .\cdk.out\AwsLambdaThumbnailizerStack.template.json thumbnailizer-lambda --profile profile-name
```

### Run and Debug

- Launch: `SAM: Thumbnailizer Lambda`
