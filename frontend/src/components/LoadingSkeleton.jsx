import React from 'react';

const SkeletonBlock = ({ className }) => (
  <div className={`bg-gray-700 rounded-md animate-pulse ${className}`} />
);

function LoadingSkeleton() {
  return (
    <div className="mt-8 p-6 bg-gray-800/50 border border-gray-700 rounded-lg">
      {/* Header Skeleton */}
      <div className="mb-6 pb-6 border-b border-gray-700">
        <SkeletonBlock className="h-12 w-3/4 mb-3" />
        <SkeletonBlock className="h-6 w-1/2" />
      </div>

      {/* Key Metrics Skeleton */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-10">
        <SkeletonBlock className="h-20" />
        <SkeletonBlock className="h-20" />
        <SkeletonBlock className="h-20" />
        <SkeletonBlock className="h-20" />
        <SkeletonBlock className="h-20" />
      </div>

      {/* Chart Skeleton */}
      <div className="mb-12 bg-gray-900/40 p-6 rounded-xl">
        <SkeletonBlock className="h-8 w-1/3 mb-4" />
        <SkeletonBlock className="h-72 w-full" />
      </div>

      {/* AI Report Skeleton */}
      <div className="mb-12">
        <SkeletonBlock className="h-8 w-1/3 mb-4" />
        <div className="p-6 bg-gray-900/40 rounded-xl space-y-4">
          <SkeletonBlock className="h-6 w-full" />
          <SkeletonBlock className="h-6 w-5/6" />
          <SkeletonBlock className="h-6 w-full" />
          <SkeletonBlock className="h-6 w-3/4" />
        </div>
      </div>
    </div>
  );
}

export default LoadingSkeleton;