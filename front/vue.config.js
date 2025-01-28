module.exports = {
  devServer: {
    host: '192.168.64.100',
    proxy: {
      '/api': {
        target: 'http://192.168.64.100:9898',
        // target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
      '/media': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true
      },
    },
  },
};