import pyspark
from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip

spark = configure_spark_with_delta_pip(
    SparkSession.builder
    .appName('training-test')
    .config('spark.driver.memory', '1g')
    .master('local[2]')
).getOrCreate()
spark.sparkContext.setLogLevel('ERROR')

df = spark.range(100)
print(f'✅ PySpark {pyspark.__version__} OK — {df.count()} registros')

import tempfile
with tempfile.TemporaryDirectory() as tmp:
    df.write.format('delta').mode('overwrite').save(tmp)
    df2 = spark.read.format('delta').load(tmp)
    print(f'✅ Delta Lake OK — {df2.count()} registros')

spark.stop()
print('✅ Teste concluído!')
