# ML Pipeline

A machine learning pipeline for training classifiers on Vertex AI. This repository provides infrastructure for training ML models on melt curve data with automated GCS artifact management.

## Overview

This pipeline trains ML classifiers to identify bacterial species from melt curve data. Training runs on Google Cloud Vertex AI with artifacts automatically synced to Cloud Storage.

### Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Vertex AI                                │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                 Custom Training Job                       │  │
│  │  ┌─────────────┐    ┌─────────────┐    ┌───────────────┐  │  │
│  │  │ Load Data   │───▶│   Train     │───▶│ Save Artifacts│  │  │
│  │  │ from GCS    │    │ Classifier  │    │ to GCS        │  │  │
│  │  └─────────────┘    └─────────────┘    └───────────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
         │                                           │
         ▼                                           ▼
┌─────────────────┐                       ┌─────────────────────┐
│   Data Bucket   │                       │  Artifacts Bucket   │
│ melio-melt-curve│                       │ melio-ml-pipeline-  │
│                 │                       │ artifacts           │
│ ├── melt_eva_db │                       │ ├── training_outputs│
│ └── well_meta_db│                       │ │   └── run_xxx/    │
└─────────────────┘                       │ │       ├── model/  │
                                          │ │       ├── outputs/│
                                          │ │       └── logs/   │
                                          │ └── scripts/        │
                                          └─────────────────────┘
```

## Repository Structure

### Current

```
ml_pipeline/
├── deploy/                        # Deployment and orchestration
│   ├── deploy_to_vertex_ai.py     # Main deployment script
│   └── setup_gcs_buckets.py       # GCS bucket setup
├── training/                      # Training scripts
│   ├── gcp_rec_plot.py            # Classifier training script
│   └── dbs.json                   # Training data configuration
├── data_migration/                # Data exploration notebooks
│   ├── check_data.ipynb
│   └── explore_gcs_data.ipynb
├── Dockerfile                     # Training container definition
├── entrypoint.sh                  # Container entrypoint
├── cloudbuild.yaml                # Cloud Build configuration
├── requirements.txt               # Python dependencies
└── README.md
```

### Future for Multi-Component Pipeline

```
ml_pipeline/
├── components/                    # Pipeline components
│   ├── training/
│   │   ├── Dockerfile
│   │   ├── train.py
│   │   └── requirements.txt
│   ├── preprocessing/             # Data preparation step
│   │   ├── Dockerfile
│   │   └── preprocess.py
│   └── evaluation/                # Model evaluation step
│       └── evaluate.py
├── pipelines/                     # Kubeflow/Vertex pipeline definitions
│   └── training_pipeline.py
├── deploy/
│   └── deploy.py
├── notebooks/
└── shared/                        # Shared utilities
    └── utils.py
```

## Cloud Storage Structure

### Data Bucket (`melio-melt-curve`)

```
melio-melt-curve/
├── melt_eva_db/                   # EVA timeseries data
│   └── {chip_id}_timeseries.parquet
└── well_meta_db/                  # Well metadata
    └── {chip_id}_metadata.parquet
```

### Artifacts Bucket (`melio-ml-pipeline-artifacts`)

```
melio-ml-pipeline-artifacts/
├── training_outputs/
│   └── run_{timestamp}/           # Each training run
│       ├── model/                 # Keras model files
│       │   └── split_{i}_model.keras
│       ├── outputs/               # Metrics and visualizations
│       │   ├── config.json
│       │   ├── run_summary.json
│       │   ├── split_{i}_metadata.json
│       │   ├── split_{i}_results.json
│       │   ├── split_{i}_report.csv
│       │   ├── split_{i}_confusion_matrix.csv
│       │   ├── split_{i}_confusion_matrix.png
│       │   └── split_{i}_confusion_matrix_pct.png
│       └── logs/                  # TensorBoard logs
│           └── split_{i}/
├── scripts/                       # Uploaded training scripts
│   └── gcp_rec_plot.py
└── staging/                       # Vertex AI staging area
```

## Prerequisites

### GCP Setup

1. **Enable APIs:**

   ```bash
   gcloud services enable aiplatform.googleapis.com
   gcloud services enable storage.googleapis.com
   gcloud services enable containerregistry.googleapis.com
   gcloud services enable cloudbuild.googleapis.com
   ```

2. **Authentication:**
   ```bash
   gcloud auth login
   gcloud auth application-default login
   gcloud config set project melt-ml
   ```

### Local Setup

1. **Required software:**

   - Python 3.13.\*
   - Docker Desktop
   - Google Cloud SDK

2. **Environment variables:**
   Create `.env` file in project root:

   ```
   GITHUB_TOKEN1=<token_for_private_packages>
   GITHUB_TOKEN2=<optional_secondary_token>
   ```

3. **Install dependencies:**
   ```bash
   pip install google-cloud-aiplatform google-cloud-storage
   ```

## Quick Start

### 1. Build and Deploy (Full Pipeline)

```bash
cd deploy
python deploy_to_vertex_ai.py
```

This will:

- Build Docker image via Cloud Build
- Push to Google Container Registry
- Submit training job to Vertex AI
- Wait for job completion

### 2. Deploy with Custom Script (Fast Iteration)

Update `deploy_to_vertex_ai.py` main function:

```python
# Comment out default job, uncomment custom script job
ret_custom = submit_training_with_script(
    image_uri=TRAINING_IMAGE_URI,
    script_path="training/gcp_rec_plot.py",
    register_model=REGISTER_MODEL
)
```

Then run:

```bash
python deploy_to_vertex_ai.py
```

### 3. Build Image Only

```bash
# Cloud Build
gcloud builds submit . \
    --project melt-ml \
    --region us-central1 \
    --config cloudbuild.yaml \
    --substitutions=_IMAGE_URI='gcr.io/melt-ml/ml-pipeline-training:v1.4',_GITHUB_TOKEN='<token>'

# Local build
docker buildx build --platform linux/amd64 \
    --build-arg GITHUB_TOKEN=<token> \
    -t gcr.io/melt-ml/ml-pipeline-training:v1.4 .

docker push gcr.io/melt-ml/ml-pipeline-training:v1.4
```

## Configuration

### Training Parameters

Edit `training/gcp_rec_plot.py`:

```python
# Chip data configuration
CHIPS = [
    {"id": "chip_id_1", "species": "E. coli"},
    {"id": "chip_id_2", "species": "K. oxytoca"},
]

# Model hyperparameters (in main())
clf_config = RecurrencePlot.Config(
    params=RecurrencePlot.ClassifierParams(
        image_width=150,
        class_labels=class_labels
    ),
    hyperparams=RecurrencePlot.ClassifierHyperParams(
        epochs=30,
        batch_size=16,
        generator_percentage=30,
        generator_threshold="distance"
    ),
)
```

### Compute Resources

Edit `deploy/deploy_to_vertex_ai.py`:

```python
MACHINE_TYPE = "n1-standard-16"      # CPU/RAM
ACCELERATOR_TYPE = "NVIDIA_TESLA_T4" # GPU type
ACCELERATOR_COUNT = 1                 # Number of GPUs
```

**Available machine types:**
| Type | vCPUs | RAM | Cost/hr |
|------|-------|-----|---------|
| `n1-standard-4` | 4 | 15GB | ~$0.19 |
| `n1-standard-8` | 8 | 30GB | ~$0.38 |
| `n1-standard-16` | 16 | 60GB | ~$0.76 |

**Available accelerators:**
| Type | Memory | Cost/hr |
|------|--------|---------|
| `NVIDIA_TESLA_T4` | 16GB | ~$0.35 |
| `NVIDIA_TESLA_V100` | 16GB | ~$2.48 |
| `NVIDIA_TESLA_A100` | 40GB | ~$3.67 |

## Monitoring

### Job Status

```bash
# List jobs
gcloud ai custom-jobs list --region=us-central1

# Job details
gcloud ai custom-jobs describe JOB_ID --region=us-central1

# Stream logs
gcloud ai custom-jobs stream-logs JOB_ID --region=us-central1
```

### View Artifacts

```bash
# List training runs
gsutil ls gs://melio-ml-pipeline-artifacts/training_outputs/

# Download outputs
gsutil -m cp -r gs://melio-ml-pipeline-artifacts/training_outputs/run_xxx/outputs/ ./local_outputs/
```

### TensorBoard

```bash
# View logs locally
tensorboard --logdir=gs://melio-ml-pipeline-artifacts/training_outputs/run_xxx/logs/
```

## Troubleshooting

### Common Issues

| Issue                       | Solution                                           |
| --------------------------- | -------------------------------------------------- |
| `gsutil: command not found` | Ensure Cloud SDK is on PATH                        |
| Docker build fails          | Start Docker Desktop                               |
| Permission denied on GCS    | Check service account roles                        |
| Out of memory               | Increase `MACHINE_TYPE` or reduce `batch_size`     |
| GPU not detected            | Verify `ACCELERATOR_TYPE` and TensorFlow GPU build |

### Debug Commands

```bash
# Test GCS access
gsutil ls gs://melio-melt-curve/

# Test Docker locally
docker run --rm gcr.io/melt-ml/ml-pipeline-training:v1.4

# Check quotas
gcloud compute project-info describe --project=melt-ml
```

## Development

### Local Testing

```bash
# Set environment variables
export DATA_BUCKET=melio-melt-curve
export EVA_DB=melt_eva_db
export META_DB=well_meta_db
export AIP_MODEL_DIR=/tmp/run/model
export AIP_TENSORBOARD_LOG_DIR=/tmp/run/logs

# Run training locally
python training/gcp_rec_plot.py
```

### Adding New Components

1. Create component directory under `components/`
2. Add Dockerfile and requirements.txt
3. Update `deploy_to_vertex_ai.py` with new image URI
4. For multi-step pipelines, create pipeline definition in `pipelines/`

## Supported Classifiers

Currently, the pipeline includes a **Recurrence Plot classifier** (`gcp_rec_plot.py`) that uses CNN-based image classification on recurrence plot representations of melt curves.

To add new classifiers:

- Add a new training script under `training/` (e.g., `training/my_classifier.py`)
- Run with pre-built image using custom script deployment:
  ```python
  submit_training_with_script(image_uri=TRAINING_IMAGE_URI, script_path="training/my_classifier.py")
  ```

The Docker image includes all dependencies from `melio-training` and TensorFlow, so new classifier scripts can be iterated without rebuilding the image.

## License

Proprietary — Internal use only. © Melio Tech

## References

- [Vertex AI Custom Training](https://cloud.google.com/vertex-ai/docs/training/overview)
- [GCS FUSE](https://cloud.google.com/storage/docs/gcs-fuse)
- [TensorFlow Keras](https://www.tensorflow.org/guide/keras)
