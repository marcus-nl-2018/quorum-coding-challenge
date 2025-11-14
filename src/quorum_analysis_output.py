import pandas as pd
import os
import argparse

def find_csv_file(keyword):
    """Find the first CSV file in the current folder containing the keyword."""
    for file in os.listdir('.'):
        if file.endswith('.csv') and keyword.lower() in file.lower():
            return file
    raise FileNotFoundError(f"No CSV file found containing '{keyword}'")

def main():
    # === Step 1: Parse command-line arguments ===
    parser = argparse.ArgumentParser(description="Quorum Coding Challenge Analysis")
    parser.add_argument("--output_folder", type=str, default=".", help="Folder to save output CSVs")
    args = parser.parse_args()
    output_folder = args.output_folder

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output folder: {output_folder}\n")

    # === Step 2: Auto-detect CSV files ===
    legislators_file = find_csv_file('legislators')
    bills_file = find_csv_file('bills')
    votes_file = find_csv_file('votes')
    vote_results_file = find_csv_file('vote_results')

    print(f"Detected CSV files:\nLegislators: {legislators_file}\nBills: {bills_file}\nVotes: {votes_file}\nVote Results: {vote_results_file}\n")

    # === Step 3: Read CSV files ===
    legislators_df = pd.read_csv(legislators_file)
    bills_df = pd.read_csv(bills_file)
    votes_df = pd.read_csv(votes_file)
    vote_results_df = pd.read_csv(vote_results_file)

    # === Step 4: Vectorized legislator support/oppose counts ===
    support_counts = vote_results_df[vote_results_df['vote_type'] == 1].groupby('legislator_id').size()
    oppose_counts = vote_results_df[vote_results_df['vote_type'] == 2].groupby('legislator_id').size()

    legislators_df['num_supported_bills'] = legislators_df['id'].map(support_counts).fillna(0).astype(int)
    legislators_df['num_opposed_bills'] = legislators_df['id'].map(oppose_counts).fillna(0).astype(int)

    # Save legislator vote summary
    legislator_csv = os.path.join(output_folder, "legislators-support-oppose-count.csv")
    legislators_df.to_csv(legislator_csv, index=False)
    print(f"Legislator vote summary saved to '{legislator_csv}'\n")

    # Display top legislators
    print("Top legislators by number of bills supported:")
    print(legislators_df.sort_values(by='num_supported_bills', ascending=False).head(5)[['name', 'num_supported_bills', 'num_opposed_bills']], "\n")
    print("Top legislators by number of bills opposed:")
    print(legislators_df.sort_values(by='num_opposed_bills', ascending=False).head(5)[['name', 'num_supported_bills', 'num_opposed_bills']], "\n")

    # === Step 5: Vectorized bill support/oppose counts ===
    vote_results_with_bill = vote_results_df.merge(votes_df[['id','bill_id']], left_on='vote_id', right_on='id', suffixes=('','_vote'))

    supporter_counts = vote_results_with_bill[vote_results_with_bill['vote_type'] == 1].groupby('bill_id').size()
    opposer_counts = vote_results_with_bill[vote_results_with_bill['vote_type'] == 2].groupby('bill_id').size()

    bills_df['supporter_count'] = bills_df['id'].map(supporter_counts).fillna(0).astype(int)
    bills_df['opposer_count'] = bills_df['id'].map(opposer_counts).fillna(0).astype(int)

    # Attach primary sponsor name
    bills_df = bills_df.merge(
        legislators_df[['id','name']],
        left_on='Primary Sponsor',
        right_on='id',
        how='left',
        suffixes=('','_sponsor')
    )
    bills_df['primary_sponsor'] = bills_df['name'].fillna("Unknown")
    bills_df = bills_df[['id','title','supporter_count','opposer_count','primary_sponsor']]

    # Save bill vote summary
    bills_csv = os.path.join(output_folder, "bills-support-oppose-count.csv")
    bills_df.to_csv(bills_csv, index=False)
    print(f"Bill vote summary saved to '{bills_csv}'\n")

    # Display top bills
    print("Top bills by number of supporters:")
    print(bills_df.sort_values(by='supporter_count', ascending=False).head(5)[['title','supporter_count','opposer_count','primary_sponsor']], "\n")
    print("Top bills by number of opposers:")
    print(bills_df.sort_values(by='opposer_count', ascending=False).head(5)[['title','supporter_count','opposer_count','primary_sponsor']], "\n")

if __name__ == "__main__":
    main()
