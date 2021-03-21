
# user-influence-analysis

## Usage

### Installation

install the requirements 

    pip install -r requirements.txt

### Configuration

1. Copy the content of the `user_influence_analysis/secret_config.examle.yaml` and create a new file named `user_influence_analysis/secret_config.yaml`
2. Obtain a Github API token and enter it under tokens section.

### Data Collection

#### Fetch Users - Followers

Firstly, user - follower relationship should be collected. Run the user follower fetching script by specifying a user as starting point. It might be a good choice to denote a user having many followers.

    python user_influence_analysis/data_collection/user_follower_collector.py --username=place_user_name_here

#### Fetch Users - Repos

It is also required to fetch repositories of users to calculate H-index.

    python user_influence_analysis/data_collection/user_repo_collector.py

#### Analyze

To run the correlation analysis which incorporates network metrics of user social network and H-index of user repositories:

    python user_influence_analysis/analysis/correlation_analysis.py

#### Visualize Results

To see the final analysis report as a plot:

    python user_influence_analysis/analysis/visualize_results.py
