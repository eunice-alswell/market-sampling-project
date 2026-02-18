"""
Market Sampling Dummy Data Generator

This script generates realistic dummy data for market sampling campaigns.
It creates data for areas, promoters, sampling events, and respondents,
and exports them to an Excel file.

Author: Eunice Alswell
Date: 2026
"""

import numpy as np
import pandas as pd
from faker import Faker
import random


def initialize_faker(seed=42):
    """
    Initialize Faker and set random seed for reproducibility.
    
    Args:
        seed (int): Random seed value
    
    Returns:
        Faker: Initialized Faker object
    """
    fake = Faker()
    random.seed(seed)
    np.random.seed(seed)
    return fake


def define_lookup_data():
    """
    Define static lookup data for sampling types, regions, age ranges, etc.
    
    Returns:
        dict: Dictionary containing all lookup data
    """
    sampling_types = ["Open Market", "Traffic", "Trade", "Third Space", "Institutional"]
    institution_types = ["Church", "Mosque"]
    regions_districts = {
        "Greater Accra": ["La Nkwantanang", "Ablekuma", "Madina", "Adenta"],
        "Ashanti": ["Kumasi Metro", "Ejisu", "Obuasi"],
        "Central": ["Cape Coast", "Kasoa", "Mankessim"]
    }
    age_ranges = ["18–24", "25–34", "35–44", "45–54", "55+"]
    toothpaste_brands = ["Pepsodent", "Kel", "Colgate", "Close-Up", "Oral-B", "Sensodyne"]
    reasons = [
        "Curious about the brand",
        "Referred by friend",
        "Free product sample",
        "Interested in survey",
        "Enjoy trying new products",
        "Promoter was convincing",
        "Happened to be available"
    ]
    
    return {
        "sampling_types": sampling_types,
        "institution_types": institution_types,
        "regions_districts": regions_districts,
        "age_ranges": age_ranges,
        "toothpaste_brands": toothpaste_brands,
        "reasons": reasons
    }


def generate_area_data(regions_districts, start_id=1001):
    """
    Generate area data with regions, districts, and areas.
    
    Args:
        regions_districts (dict): Dictionary of regions and their districts
        start_id (int): Starting ID for areas
    
    Returns:
        pd.DataFrame: DataFrame containing area data
    """
    area_records = []
    area_id = start_id
    
    for region, districts in regions_districts.items():
        for district in districts:
            for i in range(2):  # 2 areas per district
                area_records.append({
                    "areaID": f"A {area_id}",
                    "AreaName": f"{district} Area {i+1}",
                    "region": region,
                    "district": district
                })
                area_id += 1
    
    return pd.DataFrame(area_records)


def generate_promoter_data(fake, num_promoters=5, start_id=1000):
    """
    Generate promoter data with names and contact information.
    
    Args:
        fake (Faker): Faker object for generating fake data
        num_promoters (int): Number of promoters to generate
        start_id (int): Starting ID for promoters
    
    Returns:
        pd.DataFrame: DataFrame containing promoter data
    """
    promoters = [{
        "promoterID": f"P{start_id + i}",
        "name": fake.name(),
        "contact": fake.phone_number(),
    } for i in range(num_promoters)]
    
    return pd.DataFrame(promoters)


def generate_sampling_type_df(sampling_types):
    """
    Generate sampling type lookup DataFrame.
    
    Args:
        sampling_types (list): List of sampling type names
    
    Returns:
        pd.DataFrame: DataFrame containing sampling types
    """
    sampling_type_df = pd.DataFrame(sampling_types, columns=['SamplingType'])
    sampling_type_df.index = [f'ST{i}' for i in range(1, len(sampling_type_df) + 1)]
    return sampling_type_df


def generate_sampling_facts(fake, area_df, promoter_df, sampling_type_df, 
                           institution_types, toothpaste_brands, 
                           num_samples=6, start_id=1000):
    """
    Generate sampling fact table data.
    
    Args:
        fake (Faker): Faker object for generating fake data
        area_df (pd.DataFrame): Area data
        promoter_df (pd.DataFrame): Promoter data
        sampling_type_df (pd.DataFrame): Sampling type data
        institution_types (list): List of institution types
        toothpaste_brands (list): List of toothpaste brands
        num_samples (int): Number of sampling events to generate
        start_id (int): Starting ID for sampling events
    
    Returns:
        pd.DataFrame: DataFrame containing sampling fact data
    """
    sampling_facts = []
    
    for i in range(num_samples):
        area = area_df.sample(1).iloc[0]
        promoter = promoter_df.sample(1).iloc[0]
        sampling_type = random.choice(sampling_type_df.index)
        
        institution_type = random.choice(institution_types) if sampling_type == "ST5" else None
        target = random.randint(100, 200)
        passengers = random.randint(5, 10) if sampling_type == "ST2" else None
        start_date = fake.date_between(start_date='-1y', end_date='today')
        end_date = start_date + pd.Timedelta(days=30)
        
        sampling_facts.append({
            "samplingID": f"S{start_id + i}",
            "areaID": area["areaID"],
            "promoterID": promoter["promoterID"],
            "samplingType": sampling_type,
            "institutionType": institution_type,
            "target": target,
            "passengers": passengers,
            "toothpasteBrand": random.choice(toothpaste_brands),
            "startDate": start_date,
            "endDate": end_date,
        })
    
    return pd.DataFrame(sampling_facts)


def generate_respondents(fake, sampling_fact_df, area_df, age_ranges, 
                        toothpaste_brands, reasons, start_id=1000):
    """
    Generate respondent data for each sampling event.
    
    Args:
        fake (Faker): Faker object for generating fake data
        sampling_fact_df (pd.DataFrame): Sampling fact data
        area_df (pd.DataFrame): Area data
        age_ranges (list): List of age ranges
        toothpaste_brands (list): List of toothpaste brands
        reasons (list): List of participation reasons
        start_id (int): Starting ID for respondents
    
    Returns:
        pd.DataFrame: DataFrame containing respondent data
    """
    respondents = []
    respondent_id = start_id
    
    for _, sampling in sampling_fact_df.iterrows():
        # Generate random number of respondents between 100 and target
        actual = random.randint(100, sampling['target'])
        
        for _ in range(actual):
            respondents.append({
                "respondentID": f"R{respondent_id}",
                "samplingID": sampling['samplingID'],
                "fullName": fake.name(),
                "ageRange": random.choice(age_ranges),
                "contact": fake.phone_number(),
                "toothpasteBrand": sampling['toothpasteBrand'],
                "perferredBrand": random.choice(toothpaste_brands),
                "areaID": sampling['areaID'],
                "residenceArea": area_df['AreaName'].sample(1).values[0],
                "reason": random.choice(reasons),
                "optInOtherProducts": random.choice(["Yes", "No"]),
                "dateOfSubmistion": random.choice(
                    pd.date_range(sampling['startDate'], sampling['endDate'])
                ),
            })
            respondent_id += 1
    
    return pd.DataFrame(respondents)


def export_to_excel(area_df, promoter_df, sampling_fact_df, 
                   respondents_df, sampling_type_df, 
                   output_path='data/market_sampling_dummy_data.xlsx'):
    """
    Export all DataFrames to an Excel file with multiple sheets.
    
    Args:
        area_df (pd.DataFrame): Area data
        promoter_df (pd.DataFrame): Promoter data
        sampling_fact_df (pd.DataFrame): Sampling fact data
        respondents_df (pd.DataFrame): Respondent data
        sampling_type_df (pd.DataFrame): Sampling type data
        output_path (str): Path to save the Excel file
    """
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        area_df.to_excel(writer, sheet_name='Area', index=False)
        promoter_df.to_excel(writer, sheet_name='Promoter', index=False)
        sampling_fact_df.to_excel(writer, sheet_name='SamplingFact', index=False)
        respondents_df.to_excel(writer, sheet_name='Respondents', index=False)
        sampling_type_df.to_excel(writer, sheet_name='SamplingType', index=True)
    
    print(f"Dummy data generation completed and saved to '{output_path}'.")
    print(f"Generated {len(area_df)} areas, {len(promoter_df)} promoters, "
          f"{len(sampling_fact_df)} sampling events, and {len(respondents_df)} respondents.")


def main():
    """
    Main function to execute the entire data generation process.
    """
    # Initialize Faker
    fake = initialize_faker(seed=42)
    
    # Define lookup data
    lookup_data = define_lookup_data()
    
    # Generate area data
    print("Generating area data...")
    area_df = generate_area_data(lookup_data['regions_districts'])
    
    # Generate promoter data
    print("Generating promoter data...")
    promoter_df = generate_promoter_data(fake, num_promoters=5)
    
    # Generate sampling type data
    print("Generating sampling type data...")
    sampling_type_df = generate_sampling_type_df(lookup_data['sampling_types'])
    
    # Generate sampling facts
    print("Generating sampling fact data...")
    sampling_fact_df = generate_sampling_facts(
        fake, area_df, promoter_df, sampling_type_df,
        lookup_data['institution_types'],
        lookup_data['toothpaste_brands'],
        num_samples=6
    )
    
    # Generate respondents
    print("Generating respondent data...")
    respondents_df = generate_respondents(
        fake, sampling_fact_df, area_df,
        lookup_data['age_ranges'],
        lookup_data['toothpaste_brands'],
        lookup_data['reasons']
    )
    
    # Export to Excel
    print("Exporting data to Excel...")
    export_to_excel(area_df, promoter_df, sampling_fact_df, 
                   respondents_df, sampling_type_df)
    
    print("\nData generation complete!")
    print(f"Total respondents generated: {len(respondents_df)}")


if __name__ == "__main__":
    main()
