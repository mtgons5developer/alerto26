# fix_emergency_types.py
from emergencies.models import Emergency

# Map lowercase to uppercase
type_mapping = {
    'accident': 'CAR_ACCIDENT',
    'fire': 'FIRE',
    'medical': 'MEDICAL',
    'natural_disaster': 'NATURAL_DISASTER',
    'hazard': 'OTHER',
    'car_accident': 'CAR_ACCIDENT',
    'police': 'POLICE',
    'utility': 'UTILITY',
    'other': 'OTHER',
}

# Update existing records
for emergency in Emergency.objects.all():
    current_type = emergency.emergency_type
    if current_type in type_mapping:
        emergency.emergency_type = type_mapping[current_type]
        emergency.save()
        print(f"Updated {emergency.code}: {current_type} → {emergency.emergency_type}")
    elif current_type and current_type.islower():
        # Convert any lowercase to uppercase
        emergency.emergency_type = current_type.upper()
        emergency.save()
        print(f"Updated {emergency.code}: {current_type} → {emergency.emergency_type}")

print("✅ Migration complete!")