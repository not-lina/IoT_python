unpack the file
```
tar -xvf iot_gen_cnt4144-0.0.1.tar.gz
```

run the module
```
python3 iot_gen_cnt4144-0.0.1/iot_gen
```

or install from the rep
```
git clone https://github.com/not-lina/IoT_python
python3 IoT_python/iot_python
```

Included in the module is `generated.csv` which has a set of
test data that can be loaded into the module without
needing to first generate it.

- **iot_gen.py**: entry point and wx app
- **plots.py**: contains wx components for the stats charts
- **DataLoader.py**: handles generating the test data
- **UserFactory.py**: schema and factory for user
- **SensorArray.py**: schema for sensor array and sensor classes
