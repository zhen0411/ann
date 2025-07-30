import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { fetchMediaFile } from '../store/slices/mediaSlice';
import { fetchAnnotations, createAnnotation } from '../store/slices/annotationsSlice';
import { fetchLabels } from '../store/slices/labelsSlice';
import {
  PlayIcon,
  PauseIcon,
  ForwardIcon,
  BackwardIcon,
  PlusIcon,
} from '@heroicons/react/24/outline';

function Annotation() {
  const { mediaId } = useParams();
  const dispatch = useDispatch();
  const { currentMediaFile } = useSelector((state) => state.media);
  const { annotations } = useSelector((state) => state.annotations);
  const { labels } = useSelector((state) => state.labels);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [selectedLabel, setSelectedLabel] = useState('');

  useEffect(() => {
    if (mediaId) {
      dispatch(fetchMediaFile(mediaId));
      dispatch(fetchAnnotations({ media_file_id: mediaId }));
      if (currentMediaFile?.project_id) {
        dispatch(fetchLabels(currentMediaFile.project_id));
      }
    }
  }, [dispatch, mediaId, currentMediaFile?.project_id]);

  const handlePlayPause = () => {
    setIsPlaying(!isPlaying);
  };

  const handleTimeUpdate = (e) => {
    setCurrentTime(e.target.currentTime);
  };

  const handleLoadedMetadata = (e) => {
    setDuration(e.target.duration);
  };

  const handleSeek = (e) => {
    const video = e.target;
    const rect = video.getBoundingClientRect();
    const clickX = e.clientX - rect.left;
    const newTime = (clickX / rect.width) * duration;
    video.currentTime = newTime;
  };

  const formatTime = (time) => {
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };

  if (!currentMediaFile) {
    return (
      <div className="text-center py-12">
        <h3 className="text-lg font-medium text-gray-900">媒体文件不存在</h3>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto">
      <div className="mb-8">
        <h1 className="text-2xl font-semibold text-gray-900">标注工具</h1>
        <p className="mt-2 text-sm text-gray-600">
          标注文件: {currentMediaFile.original_filename}
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* 媒体播放器 */}
        <div className="lg:col-span-2">
          <div className="bg-white shadow rounded-lg p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">媒体播放器</h3>
            
            {currentMediaFile.media_type === 'video' ? (
              <video
                className="w-full rounded-lg"
                onTimeUpdate={handleTimeUpdate}
                onLoadedMetadata={handleLoadedMetadata}
                onClick={handleSeek}
              >
                <source src={`/api/media/${currentMediaFile.id}/stream`} type="video/mp4" />
                您的浏览器不支持视频播放。
              </video>
            ) : (
              <audio
                className="w-full"
                onTimeUpdate={handleTimeUpdate}
                onLoadedMetadata={handleLoadedMetadata}
                controls
              >
                <source src={`/api/media/${currentMediaFile.id}/stream`} type="audio/mpeg" />
                您的浏览器不支持音频播放。
              </audio>
            )}

            {/* 播放控制 */}
            <div className="mt-4 flex items-center justify-center space-x-4">
              <button
                onClick={handlePlayPause}
                className="p-2 rounded-full bg-blue-600 text-white hover:bg-blue-700"
              >
                {isPlaying ? (
                  <PauseIcon className="h-6 w-6" />
                ) : (
                  <PlayIcon className="h-6 w-6" />
                )}
              </button>
              <button className="p-2 rounded-full bg-gray-200 text-gray-700 hover:bg-gray-300">
                <BackwardIcon className="h-5 w-5" />
              </button>
              <button className="p-2 rounded-full bg-gray-200 text-gray-700 hover:bg-gray-300">
                <ForwardIcon className="h-5 w-5" />
              </button>
              <span className="text-sm text-gray-600">
                {formatTime(currentTime)} / {formatTime(duration)}
              </span>
            </div>

            {/* 时间轴 */}
            <div className="mt-4">
              <div className="relative">
                <div className="w-full h-2 bg-gray-200 rounded-full">
                  <div
                    className="h-2 bg-blue-600 rounded-full"
                    style={{ width: `${(currentTime / duration) * 100}%` }}
                  ></div>
                </div>
                <input
                  type="range"
                  min="0"
                  max={duration}
                  value={currentTime}
                  onChange={(e) => setCurrentTime(parseFloat(e.target.value))}
                  className="absolute inset-0 w-full h-2 opacity-0 cursor-pointer"
                />
              </div>
            </div>
          </div>
        </div>

        {/* 标注面板 */}
        <div className="lg:col-span-1">
          <div className="bg-white shadow rounded-lg p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">标注工具</h3>
            
            {/* 标签选择 */}
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                选择标签
              </label>
              <select
                value={selectedLabel}
                onChange={(e) => setSelectedLabel(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">请选择标签</option>
                {labels.map((label) => (
                  <option key={label.id} value={label.id}>
                    {label.name}
                  </option>
                ))}
              </select>
            </div>

            {/* 标注按钮 */}
            <div className="space-y-2">
              <button className="w-full flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700">
                <PlusIcon className="h-4 w-4 mr-2" />
                添加矩形标注
              </button>
              <button className="w-full flex items-center justify-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">
                <PlusIcon className="h-4 w-4 mr-2" />
                添加点标注
              </button>
              <button className="w-full flex items-center justify-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">
                <PlusIcon className="h-4 w-4 mr-2" />
                添加文本标注
              </button>
            </div>

            {/* 标注列表 */}
            <div className="mt-6">
              <h4 className="text-sm font-medium text-gray-900 mb-3">当前标注</h4>
              {annotations.length > 0 ? (
                <div className="space-y-2">
                  {annotations.map((annotation) => (
                    <div
                      key={annotation.id}
                      className="flex items-center justify-between p-2 border border-gray-200 rounded"
                    >
                      <div>
                        <span className="text-sm font-medium text-gray-900">
                          {annotation.annotation_type}
                        </span>
                        <span className="text-xs text-gray-500 ml-2">
                          {formatTime(annotation.start_time || 0)}
                        </span>
                      </div>
                      <span
                        className="w-3 h-3 rounded-full"
                        style={{
                          backgroundColor: labels.find(l => l.id === annotation.label_id)?.color || '#ccc'
                        }}
                      ></span>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-sm text-gray-500">暂无标注</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Annotation;