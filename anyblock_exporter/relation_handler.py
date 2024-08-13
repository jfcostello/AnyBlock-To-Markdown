import logging
from typing import Dict, Any, List, Tuple
from datetime import datetime, timedelta
from .config_loader import config

class RelationHandler:
    def __init__(self, json_objects: List[Dict[str, Any]]):
        self.json_objects = json_objects
        self.relation_cache = {}
        self.reference_date = datetime(2001, 1, 1)  # Reference date: January 1, 2001
        self.decode_timestamps = config.get('decode_timestamps', True)
        self.ignored_properties = config.get('ignored_properties', [])
        self.link_mode = config.get('turn_relations_into_obsidian_links', 'select')

    def convert_timestamp_if_applicable(self, value: Any) -> Tuple[str, bool]:
        is_date = False
        if self.decode_timestamps and isinstance(value, (int, float)) and len(str(int(value))) == 10:
            try:
                days_since_reference = int(value) // 86400
                date = self.reference_date + timedelta(days=days_since_reference)
                adjusted_date = date.replace(year=date.year - 31) - timedelta(days=1)
                is_date = True
                return adjusted_date.strftime("%Y-%m-%d"), is_date
            except Exception as e:
                logging.warning(f"Failed to convert timestamp {value}: {str(e)}")
        return self.get_relation_option_name(value), is_date

    def extract_relations(self, main_content: Dict[str, Any]) -> List[str]:
        relations = {}
        details = main_content['snapshot']['data']['details']
        relation_links = main_content['snapshot']['data']['relationLinks']

        for relation_link in relation_links:
            key = relation_link['key']
            if key in self.ignored_properties:
                continue  # Skip ignored relations

            value = details.get(key)
            relation_info = self.get_relation_info(key)
            relation_name = relation_info.get('name', key)

            if value is not None:
                if isinstance(value, list):
                    relations[relation_name] = [self.format_relation_value(item, key) for item in value]
                elif isinstance(value, bool):
                    relations[relation_name] = ['Yes' if value else 'No']
                else:
                    relations[relation_name] = [self.format_relation_value(value, key)]

        # Format relations
        formatted_relations = []
        for relation_name, values in relations.items():
            if len(values) == 1:
                formatted_relations.append(f"{relation_name}: {values[0]}")
            else:
                formatted_relations.append(f"{relation_name}:")
                formatted_relations.extend(f" - {value}" for value in values)

        logging.debug(f"Extracted relations: {formatted_relations}")
        return formatted_relations

    def format_relation_value(self, value: Any, key: str) -> str:
        converted_value, is_date = self.convert_timestamp_if_applicable(value)
        
        if is_date:
            return converted_value  # Return date without wrapping in links
        
        if self.link_mode == 'all':
            return f'"[[{converted_value}]]"'
        elif self.link_mode == 'select' and self.relation_has_options(key):
            return f'"[[{converted_value}]]"'
        else:
            return converted_value

    def relation_has_options(self, relation_key: str) -> bool:
        """Checks if a relation has pre-defined options."""
        for obj in self.json_objects:
            if obj.get('sbType') == 'STRelation' and obj['snapshot']['data']['details'].get('relationKey') == relation_key:
                # Check if relationFormat is 0, indicating free-form text
                if obj['snapshot']['data']['details'].get('relationFormat') == 0:
                    return False
                else:
                    return True
        return False  # Relation not found or format not specified

    def get_relation_info(self, relation_key: str) -> Dict[str, Any]:
        if relation_key in self.relation_cache:
            return self.relation_cache[relation_key]

        for obj in self.json_objects:
            if obj.get('sbType') == 'STRelation' and obj['snapshot']['data']['details'].get('relationKey') == relation_key:
                self.relation_cache[relation_key] = obj['snapshot']['data']['details']
                return self.relation_cache[relation_key]

        logging.warning(f"Relation info not found for key: {relation_key}")
        return {}

    def get_relation_option_name(self, option_id: str) -> str:
        """Retrieves the name of a relation option given its ID."""
        for obj in self.json_objects:
            if obj.get('sbType') == 'STRelationOption' and obj['snapshot']['data']['details'].get('id') == option_id:
                return obj['snapshot']['data']['details'].get('name', option_id)
        return str(option_id)  # Return the ID as a string if the name is not found