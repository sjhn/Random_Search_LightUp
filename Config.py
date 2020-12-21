import yaml


    data = yaml.load(f, Loader=yaml.FullLoader)
    print(data['logs'])