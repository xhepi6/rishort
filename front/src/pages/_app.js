import '../styles/globals.css'
import Head from 'next/head'

function MyApp({ Component, pageProps }) {
  return (
    <>
      <Head>
        <title>RiShort</title>
        <meta name="description" content="Transform long URLs into short, shareable links" />
      </Head>
      <Component {...pageProps} />
    </>
  )
}

export default MyApp
