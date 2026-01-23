from us_visa.pipeline.training_pipeline import TrainPipeline
from dotenv import load_dotenv

load_dotenv()

obj = TrainPipeline()
p = obj.run_pipeline()
print(p)