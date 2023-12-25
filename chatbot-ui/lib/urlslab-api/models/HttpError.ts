interface ValidationErrorItem {
  loc: Array<string | number>;
  msg: string;
  type: string;
}

interface HTTPValidationError {
  detail: ValidationErrorItem[];
}
