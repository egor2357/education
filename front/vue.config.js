module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: 'http://192.168.137.100:8001',
        changeOrigin: true
      },
    },
  },
};