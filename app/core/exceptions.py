from fastapi import HTTPException, status


class AppException(HTTPException):
    def __init__(
        self,
        detail: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_code: str = "INTERNAL_ERROR",
    ):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code


class ModelNotFoundError(AppException):
    def __init__(self, model_name: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Model '{model_name}' not found or not loaded",
            error_code="MODEL_NOT_FOUND",
        )


class ModelLoadError(AppException):
    def __init__(self, model_name: str, reason: str = ""):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to load model '{model_name}': {reason}",
            error_code="MODEL_LOAD_ERROR",
        )


class PredictionError(AppException):
    def __init__(self, model_name: str, reason: str = ""):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Prediction failed for model '{model_name}': {reason}",
            error_code="PREDICTION_ERROR",
        )


class PreprocessingError(AppException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            error_code="PREPROCESSING_ERROR",
        )


class InvalidInputError(AppException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            error_code="INVALID_INPUT",
        )
