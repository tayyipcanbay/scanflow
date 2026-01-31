# Generate Sample Data - Quick Guide

## 🎯 Generate Sample 3D Mesh Files and Metadata

I've created scripts to generate sample data for testing the system!

## 📋 What Gets Generated

1. **4 3D Mesh Files** (.obj format):
   - Week 0 (Baseline)
   - Week 4 (Fat loss in waist)
   - Week 8 (Fat loss + muscle gain)
   - Week 12 (Continued progress)

2. **BIA Data** (Bioelectrical Impedance Analysis):
   - Weight, BMI, Fat %, Muscle %, Water %
   - Changes over time (simulating real progress)

3. **User Metadata**:
   - Age, Gender, Country, Height
   - Activity level, Goals

## 🚀 Quick Start

### Step 1: Generate the Data

```bash
cd backend
source venv/bin/activate
python generate_sample_data.py
```

This will create:
```
sample_data/
├── meshes/
│   ├── user1_week0.obj
│   ├── user1_week4.obj
│   ├── user1_week8.obj
│   └── user1_week12.obj
├── metadata/
│   ├── user1_metadata.json
│   └── user1_bia_data.json
└── upload_mapping.json
```

### Step 2: Upload to API

**Option A: Automated Upload**
```bash
# Make sure API server is running first!
uvicorn app.main:app --reload

# In another terminal:
python upload_sample_data.py
```

**Option B: Manual Upload**
```bash
curl -X POST "http://localhost:8000/api/upload" \
  -F "file=@sample_data/meshes/user1_week0.obj" \
  -F "user_id=1"
```

Repeat for week4, week8, week12 files.

### Step 3: Test the System

After uploading, test comparisons:
```bash
# Get latest comparison
curl http://localhost:8000/api/comparison/user/1/latest

# Get insights
curl http://localhost:8000/api/insights/{comparison_id}

# Get action plans
curl http://localhost:8000/api/actions/1
```

## 📊 Sample Data Details

### BIA Data Progression

| Week | Weight | BMI | Fat % | Muscle % | Water % |
|------|--------|-----|-------|----------|---------|
| 0    | 75.0kg | 24.5| 25.0% | 35.0%    | 55.0%   |
| 4    | 73.0kg | 23.8| 22.2% | 36.2%    | 55.8%   |
| 8    | 71.0kg | 23.2| 18.6% | 37.4%    | 56.6%   |
| 12   | 69.0kg | 22.5| 15.4% | 38.6%    | 57.4%   |

### Mesh Changes Simulated

- **Week 0**: Baseline body shape
- **Week 4**: Waist reduction, thigh reduction
- **Week 8**: More waist/thigh reduction, chest/arm increase
- **Week 12**: Continued progress in all areas

## 🔄 Regenerate Data

To create new sample data:
```bash
python generate_sample_data.py
```

This will overwrite existing files with new randomized values.

## 📝 Files Created

1. **generate_sample_data.py** - Generates all sample data
2. **upload_sample_data.py** - Uploads data to API automatically
3. **sample_data/** - Directory with all generated files

## ✅ Verify Generation

After running, check:
```bash
ls -la sample_data/meshes/
ls -la sample_data/metadata/
cat sample_data/upload_mapping.json
```

You should see 4 mesh files and metadata files!

## 🎯 Next Steps

1. ✅ Generate sample data
2. ✅ Start API server
3. ✅ Upload data (automated or manual)
4. ✅ Test comparisons and visualizations
5. ✅ View in frontend!

Enjoy testing with real-looking data! 🚀

