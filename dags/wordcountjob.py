from pyspark.sql import SparkSession

# Initialize Spark session
spark = SparkSession.builder.appName("WordCountJob").getOrCreate()

# Sample text data (replace with actual data or file path)
text_data = ["hello world", "hello airflow", "hello spark", "hello python"]

# Parallelize the data into an RDD
rdd = spark.sparkContext.parallelize(text_data)

# Perform a word count operation
word_counts = rdd.flatMap(lambda line: line.split(" ")) \
                 .map(lambda word: (word, 1)) \
                 .reduceByKey(lambda a, b: a + b)

# Collect and print results
result = word_counts.collect()
for word, count in result:
    print(f"{word}: {count}")

# Stop the Spark session
spark.stop()