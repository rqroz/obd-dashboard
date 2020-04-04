const DEV_MODE = process.env.NODE_ENV === 'development';

module.exports = {
  transpileDependencies: [
    'vuetify'
  ],
  publicPath: DEV_MODE ? 'http://localhost:8080/' : '/',
  outputDir: `../dist`,
  devServer: {
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, PATCH, OPTIONS',
      'Access-Control-Allow-Headers': 'X-Requested-With, content-type, Authorization'
    }
  },
};
