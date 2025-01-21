export default async (axios, url, payload) => {
  try {
      let res = await axios.post(url, payload);
      return res
    } catch (e) {
      if (e.response) {
        return e.response
      } else {
        return e
      }
    }
}