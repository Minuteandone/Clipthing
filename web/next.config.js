/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  basePath: '/Clipthing',
  assetPrefix: '/Clipthing/',
  images: {
    unoptimized: true,
  },
  trailingSlash: true,
}

module.exports = nextConfig
