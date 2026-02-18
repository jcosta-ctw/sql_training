"""
NYC Yellow Taxi Data Setup for SQL Training
Downloads REAL NYC Yellow Taxi data from TLC and loads into DuckDB
Data source: https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
"""

import duckdb
import requests
from datetime import datetime

def download_zone_lookup():
    """
    Download the official NYC Taxi Zone Lookup table
    """
    print("📥 Downloading NYC Taxi Zone Lookup...")
    
    zone_url = "https://d37ci6vzurychx.cloudfront.net/misc/taxi+_zone_lookup.csv"
    
    try:
        response = requests.get(zone_url, timeout=30)
        response.raise_for_status()
        
        # Save to temp file
        with open('/tmp/taxi_zone_lookup.csv', 'wb') as f:
            f.write(response.content)
        
        print("   ✓ Zone lookup downloaded")
        return True
    except Exception as e:
        print(f"   ⚠️  Could not download zone lookup: {e}")
        print("   ℹ️  Will create minimal zone data")
        return False

def create_minimal_zones(con):
    """
    Create minimal zone data if download fails
    """
    print("\n📍 Creating minimal zone data...")
    
    con.execute("""
        CREATE TABLE zones (
            location_id INTEGER PRIMARY KEY,
            zone_name VARCHAR,
            borough VARCHAR,
            service_zone VARCHAR
        )
    """)
    
    # Insert some common zones
    zones_data = [
        (1, 'Newark Airport', 'EWR', 'EWR'),
        (4, 'Alphabet City', 'Manhattan', 'Yellow Zone'),
        (12, 'Battery Park', 'Manhattan', 'Yellow Zone'),
        (13, 'Battery Park City', 'Manhattan', 'Yellow Zone'),
        (43, 'Central Park', 'Manhattan', 'Yellow Zone'),
        (45, 'Chinatown', 'Manhattan', 'Yellow Zone'),
        (79, 'East Village', 'Manhattan', 'Yellow Zone'),
        (87, 'Financial District North', 'Manhattan', 'Yellow Zone'),
        (88, 'Financial District South', 'Manhattan', 'Yellow Zone'),
        (100, 'Garment District', 'Manhattan', 'Yellow Zone'),
        (107, 'Gramercy', 'Manhattan', 'Yellow Zone'),
        (113, 'Greenwich Village North', 'Manhattan', 'Yellow Zone'),
        (114, 'Greenwich Village South', 'Manhattan', 'Yellow Zone'),
        (125, 'Hell\'s Kitchen', 'Manhattan', 'Yellow Zone'),
        (137, 'Kips Bay', 'Manhattan', 'Yellow Zone'),
        (140, 'Lenox Hill East', 'Manhattan', 'Yellow Zone'),
        (141, 'Lenox Hill West', 'Manhattan', 'Yellow Zone'),
        (142, 'Lincoln Square East', 'Manhattan', 'Yellow Zone'),
        (143, 'Lincoln Square West', 'Manhattan', 'Yellow Zone'),
        (144, 'Little Italy', 'Manhattan', 'Yellow Zone'),
        (148, 'Lower East Side', 'Manhattan', 'Yellow Zone'),
        (161, 'Midtown Center', 'Manhattan', 'Yellow Zone'),
        (162, 'Midtown East', 'Manhattan', 'Yellow Zone'),
        (163, 'Midtown North', 'Manhattan', 'Yellow Zone'),
        (164, 'Midtown South', 'Manhattan', 'Yellow Zone'),
        (170, 'Murray Hill', 'Manhattan', 'Yellow Zone'),
        (186, 'Penn Station', 'Manhattan', 'Yellow Zone'),
        (224, 'Times Square', 'Manhattan', 'Yellow Zone'),
        (229, 'Tribeca', 'Manhattan', 'Yellow Zone'),
        (230, 'Two Bridges', 'Manhattan', 'Yellow Zone'),
        (231, 'UN/Turtle Bay South', 'Manhattan', 'Yellow Zone'),
        (232, 'Union Square', 'Manhattan', 'Yellow Zone'),
        (233, 'Upper East Side North', 'Manhattan', 'Yellow Zone'),
        (234, 'Upper East Side South', 'Manhattan', 'Yellow Zone'),
        (236, 'Upper West Side North', 'Manhattan', 'Yellow Zone'),
        (237, 'Upper West Side South', 'Manhattan', 'Yellow Zone'),
        (249, 'Yorkville East', 'Manhattan', 'Yellow Zone'),
        (250, 'Yorkville West', 'Manhattan', 'Yellow Zone'),
    ]
    
    for zone in zones_data:
        con.execute("INSERT INTO zones VALUES (?, ?, ?, ?)", zone)
    
    print(f"   ✓ Created {len(zones_data)} zones")

def setup_database(db_path='nyc_taxi.duckdb', months_to_load=3):
    """
    Create DuckDB database with REAL NYC Yellow Taxi data
    
    Parameters:
    - db_path: Path to DuckDB database file
    - months_to_load: Number of recent months to load (1-12)
    """
    print(f"\n{'='*70}")
    print("NYC Yellow Taxi SQL Training - Database Setup")
    print("Using REAL data from NYC Taxi & Limousine Commission")
    print(f"{'='*70}\n")
    
    # Create connection
    print(f"🗄️  Creating DuckDB database: {db_path}")
    con = duckdb.connect(db_path)
    
    # Set memory limit
    con.execute("SET memory_limit='2GB'")
    
    # Download and load zones
    zones_downloaded = download_zone_lookup()
    
    print("\n📍 Creating zones table...")
    con.execute("DROP TABLE IF EXISTS zones")
    
    if zones_downloaded:
        try:
            con.execute("""
                CREATE TABLE zones AS 
                SELECT 
                    LocationID as location_id,
                    Zone as zone_name,
                    Borough as borough,
                    service_zone
                FROM read_csv_auto('/tmp/taxi_zone_lookup.csv')
            """)
            zone_count = con.execute("SELECT COUNT(*) FROM zones").fetchone()[0]
            print(f"   ✓ Loaded {zone_count} zones from official TLC data")
        except Exception as e:
            print(f"   ⚠️  Error loading zones: {e}")
            create_minimal_zones(con)
    else:
        create_minimal_zones(con)
    
    # Determine which months to download
    # We'll use recent months - Yellow Taxi data is available from 2009 onwards
    # For training purposes, we'll use recent data (2024)
    
    current_year = 2024
    months = []
    
    # Start from January 2024, load the requested number of months
    for i in range(months_to_load):
        month = i + 1
        if month <= 12:
            months.append((current_year, month))
    
    print(f"\n🚕 Loading Yellow Taxi trip data...")
    print(f"   Months to load: {len(months)}")
    
    # Create trips table
    print("\n   Creating trips table structure...")
    con.execute("DROP TABLE IF EXISTS trips")
    
    # Load data directly from Parquet files on NYC TLC server
    # DuckDB can read Parquet files directly from HTTPS!
    
    urls = []
    for year, month in months:
        url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year}-{month:02d}.parquet"
        urls.append(url)
        print(f"   📦 {year}-{month:02d}")
    
    try:
        # Create table from first file
        print("\n   📊 Loading data (this may take a few minutes)...")
        
        first_url = urls[0]
        print(f"   ⏳ Reading {first_url.split('/')[-1]}...")
        
        # Create table with proper column names and types
        con.execute(f"""
            CREATE TABLE trips AS 
            SELECT 
                ROW_NUMBER() OVER () as trip_id,
                tpep_pickup_datetime as pickup_datetime,
                tpep_dropoff_datetime as dropoff_datetime,
                PULocationID as pickup_location_id,
                DOLocationID as dropoff_location_id,
                passenger_count,
                trip_distance,
                fare_amount,
                tip_amount,
                total_amount,
                payment_type
            FROM read_parquet('{first_url}')
            WHERE fare_amount > 0 
              AND fare_amount < 500
              AND trip_distance > 0
              AND trip_distance < 100
              AND passenger_count > 0
              AND passenger_count <= 6
            LIMIT 100000
        """)
        
        print(f"      ✓ Loaded data from {first_url.split('/')[-1]}")
        
        # Load additional months if requested
        for url in urls[1:]:
            try:
                print(f"   ⏳ Reading {url.split('/')[-1]}...")
                con.execute(f"""
                    INSERT INTO trips 
                    SELECT 
                        ROW_NUMBER() OVER () + (SELECT MAX(trip_id) FROM trips) as trip_id,
                        tpep_pickup_datetime as pickup_datetime,
                        tpep_dropoff_datetime as dropoff_datetime,
                        PULocationID as pickup_location_id,
                        DOLocationID as dropoff_location_id,
                        passenger_count,
                        trip_distance,
                        fare_amount,
                        tip_amount,
                        total_amount,
                        payment_type
                    FROM read_parquet('{url}')
                    WHERE fare_amount > 0 
                      AND fare_amount < 500
                      AND trip_distance > 0
                      AND trip_distance < 100
                      AND passenger_count > 0
                      AND passenger_count <= 6
                    LIMIT 50000
                """)
                print(f"      ✓ Loaded data from {url.split('/')[-1]}")
            except Exception as e:
                print(f"      ⚠️  Could not load {url.split('/')[-1]}: {e}")
                print(f"      ℹ️  Continuing with available data...")
        
        # Verify data
        print("\n📊 Verifying data...")
        trip_count = con.execute("SELECT COUNT(*) FROM trips").fetchone()[0]
        zone_count = con.execute("SELECT COUNT(*) FROM zones").fetchone()[0]
        print(f"   ✓ Trips table: {trip_count:,} rows")
        print(f"   ✓ Zones table: {zone_count} rows")
        
        # Show sample data
        print("\n🔍 Sample trip data:")
        sample = con.execute("""
            SELECT 
                pickup_datetime,
                passenger_count,
                trip_distance,
                fare_amount,
                tip_amount,
                payment_type
            FROM trips 
            LIMIT 5
        """).df()
        print(sample.to_string(index=False))
        
        # Show date range
        print("\n📅 Data date range:")
        date_range = con.execute("""
            SELECT 
                MIN(pickup_datetime) as earliest_trip,
                MAX(pickup_datetime) as latest_trip,
                COUNT(DISTINCT DATE_TRUNC('day', pickup_datetime)) as days_of_data
            FROM trips
        """).df()
        print(date_range.to_string(index=False))
        
        # Show summary statistics
        print("\n📈 Trip statistics:")
        stats = con.execute("""
            SELECT 
                COUNT(*) as total_trips,
                ROUND(AVG(fare_amount), 2) as avg_fare,
                ROUND(SUM(fare_amount), 2) as total_revenue,
                ROUND(AVG(trip_distance), 2) as avg_distance,
                ROUND(AVG(tip_amount), 2) as avg_tip
            FROM trips
        """).df()
        print(stats.to_string(index=False))
        
        # Show top pickup locations
        print("\n🏙️  Top 5 pickup zones:")
        top_zones = con.execute("""
            SELECT 
                z.zone_name,
                z.borough,
                COUNT(*) as num_pickups
            FROM trips t
            INNER JOIN zones z ON t.pickup_location_id = z.location_id
            GROUP BY z.zone_name, z.borough
            ORDER BY num_pickups DESC
            LIMIT 5
        """).df()
        print(top_zones.to_string(index=False))
        
        # Show payment type distribution
        print("\n💳 Payment types:")
        payment_types = con.execute("""
            SELECT 
                CASE 
                    WHEN payment_type = 1 THEN 'Credit Card'
                    WHEN payment_type = 2 THEN 'Cash'
                    WHEN payment_type = 3 THEN 'No Charge'
                    WHEN payment_type = 4 THEN 'Dispute'
                    ELSE 'Unknown'
                END as payment_method,
                COUNT(*) as num_trips,
                ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as percentage
            FROM trips
            GROUP BY payment_type
            ORDER BY num_trips DESC
        """).df()
        print(payment_types.to_string(index=False))
        
    except Exception as e:
        print(f"\n❌ Error loading trip data: {e}")
        print("\n⚠️  This could be due to:")
        print("   • Network connectivity issues")
        print("   • NYC TLC server temporarily unavailable")
        print("   • Data format changes")
        print("\n💡 Try again later or check: https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page")
        con.close()
        return False
    
    con.close()
    
    print(f"\n{'='*70}")
    print("✅ Database setup complete!")
    print(f"{'='*70}")
    print(f"\n📁 Database file: {db_path}")
    print(f"📊 Total trips: {trip_count:,}")
    print(f"🗺️  Total zones: {zone_count}")
    
    print("\n🚀 Next steps:")
    print("1. Open DBeaver")
    print("2. Create new DuckDB connection")
    print("3. Point to:", db_path)
    print("4. Start querying with real NYC taxi data!\n")
    
    print("💡 Example query to try:")
    print("   SELECT z.zone_name, COUNT(*) as trips")
    print("   FROM trips t")
    print("   JOIN zones z ON t.pickup_location_id = z.location_id")
    print("   GROUP BY z.zone_name")
    print("   ORDER BY trips DESC")
    print("   LIMIT 10;\n")
    
    return True

if __name__ == "__main__":
    import sys
    
    print("\n" + "="*70)
    print("NYC Yellow Taxi Data Loader")
    print("="*70)
    print("\nThis script downloads REAL NYC Yellow Taxi data from the")
    print("NYC Taxi & Limousine Commission (TLC) official data source.")
    print("\nData source: https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page")
    print("\nℹ️  Note: This will download data from the internet.")
    print("   Depending on your connection, this may take a few minutes.")
    print("="*70 + "\n")
    
    # Ask user how many months to load
    try:
        months_input = input("How many months of data to load? (1-12, default=3): ").strip()
        if months_input == "":
            months_to_load = 3
        else:
            months_to_load = int(months_input)
            if months_to_load < 1:
                months_to_load = 1
            elif months_to_load > 12:
                months_to_load = 12
    except (ValueError, KeyboardInterrupt):
        print("\nUsing default: 3 months")
        months_to_load = 3
    
    print(f"\n📅 Will load {months_to_load} month(s) of data")
    print("   (Limited to ~100K trips per month for training purposes)\n")
    
    # Run setup
    success = setup_database(db_path='nyc_taxi.duckdb', months_to_load=months_to_load)
    
    if success:
        print("\n✨ Success! Your database is ready for SQL training!")
        sys.exit(0)
    else:
        print("\n⚠️  Setup encountered issues. Please try again.")
        sys.exit(1)
