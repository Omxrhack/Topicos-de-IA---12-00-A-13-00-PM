from database import get_connection

def find_owner_by_plate(plate):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT owners.name,
               owners.phone,
               owners.email,
               vehicles.brand,
               vehicles.model,
               vehicles.year
        FROM vehicles
        INNER JOIN owners ON vehicles.owner_id = owners.id
        WHERE UPPER(vehicles.plate) = UPPER(?)
    """, (plate,))

    result = cursor.fetchone()
    conn.close()

    if not result:
        return None

    return {
        "owner_name": result["name"],
        "owner_phone": result["phone"],
        "owner_email": result["email"],
        "vehicle_brand": result["brand"],
        "vehicle_model": result["model"],
        "vehicle_year": result["year"],
    }
