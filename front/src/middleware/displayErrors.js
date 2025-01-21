export default (message, errorData, fields) => {
  Object.keys(errorData).forEach((key) => {
    let inFields = false;
    fields.forEach((field) => {
      if (field.name === key) {
        inFields = true;
      }
    });
    if (!inFields) {
      message.error(errorData[key]);
    }
  });
};
