"use client";
import { NewsFeedError } from "@/components/news-feed-error/NewsFeedError";
import { NewsFeedSkeleton } from "@/components/news-feed-skeleton/NewsFeedSkeleton";
import { NewsPostCard } from "@/components/news-post-card/NewsPostCard";
import { STRINGS } from "@/constants/strings";
import { useNewsPosts } from "@/hooks/use-news-posts";

import styles from "./page.module.css";

export default function Home() {
  const { isLoading, isError, newsPosts } = useNewsPosts();

  const renderContent = () => {
    if (isError) {
      return <NewsFeedError />;
    }

    if (isLoading) {
      return <NewsFeedSkeleton />;
    }

    return (
      <section
        className={styles.feed}
        aria-label={STRINGS.newsFeed.ariaLabel}
      >
        {newsPosts.map((newsPost) => (
          <NewsPostCard
            key={newsPost.id}
            newsPost={newsPost}
          />
        ))}
      </section>
    );
  };

  return (
    <div className={styles.page}>
      <header className={styles.header}>
        <h1 className={styles.title}>{STRINGS.newsFeed.title}</h1>
        <p className={styles.subtitle}>{STRINGS.newsFeed.subtitle}</p>
      </header>
      <main className={styles.main}>{renderContent()}</main>
    </div>
  );
}
