import requests
from flask import current_app, session

class MEDMService:
    @staticmethod
    def get_headers():
        return {
            'Authorization': f"Bearer {session.get('access_token', '')}",
            'Content-Type': 'application/json'
        }

    @classmethod
    def execute_query(cls, query, variables=None):
        payload = {"query": query}
        if variables:
            payload["variables"] = variables
        
        response = requests.post(
            current_app.config['GRAPHQL_URL'],
            headers=cls.get_headers(),
            json=payload
        )
        return response.json()

    @classmethod
    def get_collections(cls, limit=50):
        query = """
        query GetCollections($input: CollectionsInput!) {
          collections(input: $input) {
            collections {
              id
              name
            }
          }
        }
        """
        variables = {"input": {"pagination": {"limit": limit}}}
        return cls.execute_query(query, variables)

    @classmethod
    def get_projects(cls, collection_id):
        query = """
        query GetProjects($input: ProjectsByCollectionIdInput!) {
          projectsByCollectionId(input: $input) {
            projects {
              id
              name
            }
          }
        }
        """
        variables = {"input": {"collectionId": collection_id}}
        return cls.execute_query(query, variables)

    @classmethod
    def get_assets(cls, project_id):
        query = """
        query GetAssets($input: AssetsByProjectIdInput!) {
          assetsByProjectId(input: $input) {
            assets {
              id
              name
              assetTypeIds
              parentId
              components {
                name
              }
            }
          }
        }
        """
        variables = {"input": {"projectId": project_id}}
        return cls.execute_query(query, variables)
