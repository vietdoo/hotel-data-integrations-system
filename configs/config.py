# Configuration for suppliers
supplier_config = {
    'endpoint': {
        # Acme supplier API endpoint
        'acme': 'https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/acme',

        # Patagonia supplier API endpoint
        'patagonia': 'https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/patagonia',

        # Paperflies supplier API endpoint
        'paperflies': 'https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/paperflies'
    },
}

# Configuration for merging logic
merger_config = {
    'bias_factors': {
        'confidence_level': {
            # Confidence level for each supplier
            'acme': 0.9,
            'patagonia': 0.9,
            'paperflies': 0.9
        }
    },
    'unmerged_attrs': [
        # Attributes that should not be merged and remain distinct for each source
        'source'
    ],
    'source_attr_name': 'source'  # Attribute name to indicate the data's source
}
