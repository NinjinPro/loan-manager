

def json_response(
    	error: boolean|None = None,
        message: str|None = None,
        results: dict|list|str|None = None,
        **others,
    ) -> dict:
    
    return {
        'error': error,
        'message': message,
        'results': results
        **others
    }