module.exports = {
  devServer: {
    // host: '82.146.55.188',
    proxy: {
      '/api': {
        // target: 'http://82.146.55.188:9898',
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
      '/media': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true
      },
    },
  },
};