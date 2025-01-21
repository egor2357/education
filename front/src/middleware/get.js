export default async (axios, url) => {
  try {
      let res = await axios.get(url);
      return res
    } catch (e) {
      if (e.response) {
        return e.response
      } else {
        return e
      }
    }
}