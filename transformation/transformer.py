import json
from jsonata import Jsonata
import logging

logger = logging.getLogger(__name__)

class Transformer:
    
    def __init__(self, transformation_spec: str = None, spec_file=None):
        """
        Initializes the Transformer with the given transformation specification or a file containing the specification.
        Use https://pypi.org/project/jsonata-python/
        :param transformation_spec: A dictionary representing the JSON transformation specification.
        :param spec_file: A file path to a JSON file containing the transformation specification.
        """
        if spec_file:
            with open(spec_file, 'r') as file:
                transformation_spec = json.load(file)
        elif transformation_spec is None:
            raise ValueError("Either transformation_spec or spec_file must be provided")
        
        #transformation_spec_str = json.dumps(transformation_spec)
        print(f"Transformation spec transformation_spec {transformation_spec}")
        
        self.expression = Jsonata(transformation_spec)

    def transform(self, input_payload):
        """
        Transforms the input JSON payload according to the transformation specification.

        :param input_payload: A dictionary representing the input JSON payload.
        :return: A dictionary representing the transformed JSON payload.
        """
        logger.debug(f"tranforming given payload {input_payload}")
        response = self.expression.evaluate(input_payload)
        print(f"Transformation response {response}")
        logger.debug(f"Transormed response  {response}")
        return response

# Example usage
if __name__ == "__main__":
    # Sample input JSON payload
    input_payload = {
        "user": {
            "name": "John Doe",
            "age": 30,
            "email": "john.doe@example.com",
            "address": {
                "city": "New York",
                "zipcode": "10001"
            }
        },
        "orders": [
            {
                "id": "order1",
                "total": 150.00,
                "items": [
                    {"name": "Item 1", "quantity": 1},
                    {"name": "Item 2", "quantity": 2}
                ]
            },
            {
                "id": "order2",
                "total": 200.00,
                "items": [
                    {"name": "Item 3", "quantity": 3}
                ]
            }
        ]
    }

    # Option 1: Use a transformation specification directly
    transformation_spec = '''
    {
        "name": user.name,
        "ageInYears": user.age,
        "emailAddress": user.email,
        "location": {
            "city": user.address.city,
            "postalCode": user.address.zipcode
        },
        "orderSummaries": orders.{
            "orderId": id,
            "totalAmount": total,
            "itemNames": items.name
        },
        "isAdult": user.age >= 18,
        "staticValue": "This is a static value"
    }
    '''

    # Initialize Transformer with transformation specification
    transformer = Transformer(transformation_spec=transformation_spec)
    transformed_payload = transformer.transform(input_payload)
    
    # OR

    # Option 2: Use a transformation specification from a file
    #spec_file = 'transformation_spec.json'
    #transformer = Transformer(spec_file=spec_file)

    # Perform the transformation
    #transformed_payload = transformer.transform(input_payload)

    # Print the transformed output
    #print(json.dumps(transformed_payload, indent=2))
