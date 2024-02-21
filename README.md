# Sagah Bot

## Description
This is a bot that will help automate the process of filling forms for Sagah Catalog.

## Installation 
1. Clone the 

2. Install the requirements
```bash
pip install -r requirements.txt
```

3. Copy the conf-dist.ini file to conf.ini and fill in the required fields
```bash
$ cp conf-dist.ini conf.ini
```
4. Run the bot
```bash
$ python main.py operation
```

## Supported Operations
- `cursos`: find and fill the form for registering courses
- `disciplinas`: fill out the discipline form
- `professores`: fill out the professor form

### Example
```bash
$ python main.py cursos
```

## License
[MIT](https://choosealicense.com/licenses/mit/)