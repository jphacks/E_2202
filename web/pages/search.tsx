import type { NextPage } from 'next'
import Head from 'next/head'
import styles from '../styles/Home.module.css'

const Search: NextPage = () => {
    return (
        <div className={styles.container}>
            <Head>
                <title>Search</title>
            </Head>

            <main className={styles.main}>
                <h1 className={styles.title}>
                    Search
                </h1>
            </main>

            <footer className={styles.footer}>
                <a
                href="https://vercel.com?utm_source=create-next-app&utm_medium=default-template&utm_campaign=create-next-app"
                target="_blank"
                rel="noopener noreferrer"
                >
                Powered by ジーマーミ豆腐
                </a>
            </footer>
        </div>
    )
}

export default Search