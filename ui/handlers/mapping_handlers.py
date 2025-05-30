# ui/handlers/mapping_handlers.py
"""
Mapping callback handlers - extracted from mapping_callbacks.py
Separated business logic from UI definitions
"""

import json
from dash import Input, Output, State, no_update
from dash.dependencies import ALL

# Import UI components
from ui.components.mapping import create_mapping_component, create_mapping_validator
from styles.style_config import COLORS


class MappingHandlers:
    """Handles all mapping-related callbacks and business logic"""
    
    def __init__(self, app, mapping_component=None):
        self.app = app
        self.mapping_component = mapping_component or create_mapping_component()
        self.validator = create_mapping_validator()
        
    def register_callbacks(self):
        """Register all mapping-related callbacks"""
        self._register_mapping_confirmation_handler()
        self._register_classification_toggle_handler()
        # Temporarily comment out validation handler until layout is updated
        # self._register_mapping_validation_handler()
        
    def _register_mapping_confirmation_handler(self):
        """Handles mapping confirmation and shows next step"""
        @self.app.callback(
            [
                Output('mapping-ui-section', 'style'),  
                Output('entrance-verification-ui-section', 'style', allow_duplicate=True),
                Output('column-mapping-store', 'data'),
                Output('processing-status', 'children', allow_duplicate=True),
                Output('confirm-header-map-button', 'style', allow_duplicate=True),
            ],
            Input('confirm-header-map-button', 'n_clicks'),
            [
                State({'type': 'mapping-dropdown', 'index': ALL}, 'value'),
                State({'type': 'mapping-dropdown', 'index': ALL}, 'id'),
                State('csv-headers-store', 'data'),
                State('column-mapping-store', 'data')
            ],
            prevent_initial_call=True
        )
        def confirm_mapping_and_show_next_step(n_clicks, values, ids, csv_headers, existing_json):
            if not n_clicks:
                return no_update, no_update, no_update, no_update, no_update
                
            # Process the mapping
            result = self._process_mapping_confirmation(values, ids, csv_headers, existing_json)
            
            if result['success']:
                return self._create_mapping_success_response(result)
            else:
                return self._create_mapping_error_response(result)
    
    def _register_classification_toggle_handler(self):
        """Handles the manual door classification toggle functionality"""
        @self.app.callback(
            Output('door-classification-table-container', 'style'),
            Input('manual-map-toggle', 'value'),
            prevent_initial_call=False
        )
        def toggle_classification_tools(manual_map_choice):
            """Show/hide classification tools based on toggle selection"""
            # Define the styles for visibility
            hide_style = {'display': 'none'}
            show_style = {'display': 'block'}

            if manual_map_choice == 'yes':
                return show_style
            else:
                return hide_style
    
    def _process_mapping_confirmation(self, values, ids, csv_headers, existing_json):
        """Process the mapping confirmation logic"""
        try:
            # Create mapping dictionary
            mapping = {
                dropdown_value: dropdown_id['index']
                for dropdown_value, dropdown_id in zip(values, ids)
                if dropdown_value
            }
            
            # Validate mapping
            validation_result = self.validator.validate_mapping(mapping)
            
            if not validation_result['is_valid']:
                return {
                    'success': False,
                    'error': validation_result['message'],
                    'missing_columns': validation_result['missing_columns']
                }
            
            # Update stored mappings
            updated_mappings = self._update_stored_mappings(
                mapping, csv_headers, existing_json
            )
            
            return {
                'success': True,
                'mapping': mapping,
                'updated_mappings': updated_mappings,
                'csv_headers': csv_headers
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Error processing mapping: {str(e)}"
            }
    
    def _update_stored_mappings(self, mapping, csv_headers, existing_json):
        """Update the stored column mappings"""
        if isinstance(existing_json, str):
            updated_mappings = json.loads(existing_json)
        else:
            updated_mappings = existing_json or {}
        
        # Create header key for this CSV structure
        header_key = json.dumps(sorted(csv_headers)) if csv_headers else None
        
        if header_key:
            updated_mappings[header_key] = mapping
        
        return updated_mappings
    
    def _create_mapping_success_response(self, result):
        """Create response for successful mapping confirmation"""
        hide_mapping_style = {'display': 'none'}
        
        show_entrance_verification_style = {
            'display': 'block', 
            'width': '95%', 
            'margin': '0 auto', 
            'paddingLeft': '15px', 
            'boxSizing': 'border-box', 
            'textAlign': 'center'
        }
        
        hide_button_style = {'display': 'none'}
        
        status_message = "Step 2: Set Classification Options"
        
        return (
            hide_mapping_style,                    # Hide mapping UI
            show_entrance_verification_style,      # Show entrance verification UI
            result['updated_mappings'],            # Save updated mappings
            status_message,                        # Update status message
            hide_button_style                      # Hide confirm button
        )
    
    def _create_mapping_error_response(self, result):
        """Create response for mapping errors"""
        # Keep current states but update status
        error_message = f"Mapping Error: {result.get('error', 'Unknown error')}"
        
        return (
            no_update,      # Keep mapping UI visible
            no_update,      # Don't show next step
            no_update,      # Don't update mappings
            error_message,  # Show error message
            no_update       # Keep button state
        )


# Factory functions for easy handler creation
def create_mapping_handlers(app, mapping_component=None):
    """Factory function to create mapping handlers"""
    return MappingHandlers(app, mapping_component)