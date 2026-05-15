import joblib
import os

# Load the model
model_path = os.path.join('ml_training', 'models', 'crop_model_best.pkl')
model = joblib.load(model_path)

# Check what classes the model knows about
if hasattr(model, 'classes_'):
    print("✅ Model Classes:")
    for i, crop in enumerate(model.classes_):
        print(f"  {i}: {crop}")
    
    print(f"\nTotal classes: {len(model.classes_)}")
    
    if 'coffee' in [c.lower() for c in model.classes_]:
        print("\n❌ ERROR: Coffee IS in the model classes!")
    else:
        print("\n✅ Coffee is NOT in model classes (good!)")
else:
    print("❌ Model doesn't have classes_ attribute")

# Check if there's a label encoder
if hasattr(model, 'steps'):
    for name, step in model.steps:
        if hasattr(step, 'classes_'):
            print(f"\n✅ {name} classes: {step.classes_}")