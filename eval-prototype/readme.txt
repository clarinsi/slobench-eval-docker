# Build docker image:
docker build -t eval-prototype .

# Run mock evaluation
docker run -it --name eval-container-1 --rm -v /submission.json.zip:/submission.zip -v /submission.json.zip:/test_dataset.zip eval-prototype test_dataset.zip submission.zip