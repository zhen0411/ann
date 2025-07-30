import React, { useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { fetchProject } from '../store/slices/projectsSlice';
import { fetchMediaFiles } from '../store/slices/mediaSlice';
import { fetchLabels } from '../store/slices/labelsSlice';
import {
  FolderIcon,
  VideoCameraIcon,
  MusicalNoteIcon,
  TagIcon,
  UserGroupIcon,
} from '@heroicons/react/24/outline';

function ProjectDetail() {
  const { id } = useParams();
  const dispatch = useDispatch();
  const { currentProject, loading } = useSelector((state) => state.projects);
  const { mediaFiles } = useSelector((state) => state.media);
  const { labels } = useSelector((state) => state.labels);

  useEffect(() => {
    if (id) {
      dispatch(fetchProject(id));
      dispatch(fetchMediaFiles({ project_id: id }));
      dispatch(fetchLabels(id));
    }
  }, [dispatch, id]);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!currentProject) {
    return (
      <div className="text-center py-12">
        <h3 className="text-lg font-medium text-gray-900">项目不存在</h3>
      </div>
    );
  }

  const videoFiles = mediaFiles.filter(file => file.media_type === 'video');
  const audioFiles = mediaFiles.filter(file => file.media_type === 'audio');

  return (
    <div>
      <div className="mb-8">
        <div className="flex items-center">
          <FolderIcon className="h-8 w-8 text-blue-500 mr-3" />
          <div>
            <h1 className="text-2xl font-semibold text-gray-900">
              {currentProject.name}
            </h1>
            <p className="text-sm text-gray-600 mt-1">
              {currentProject.description || '暂无描述'}
            </p>
          </div>
        </div>
      </div>

      {/* 项目统计 */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-8">
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <VideoCameraIcon className="h-6 w-6 text-blue-500" />
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    视频文件
                  </dt>
                  <dd className="text-lg font-medium text-gray-900">
                    {videoFiles.length}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <MusicalNoteIcon className="h-6 w-6 text-green-500" />
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    音频文件
                  </dt>
                  <dd className="text-lg font-medium text-gray-900">
                    {audioFiles.length}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <TagIcon className="h-6 w-6 text-purple-500" />
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    标签数量
                  </dt>
                  <dd className="text-lg font-medium text-gray-900">
                    {labels.length}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <UserGroupIcon className="h-6 w-6 text-yellow-500" />
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    项目状态
                  </dt>
                  <dd className="text-lg font-medium text-gray-900">
                    {currentProject.is_active ? '活跃' : '非活跃'}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* 媒体文件列表 */}
      <div className="bg-white shadow rounded-lg mb-8">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
            媒体文件
          </h3>
          {mediaFiles.length > 0 ? (
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {mediaFiles.map((file) => (
                <div
                  key={file.id}
                  className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50"
                >
                  <div className="flex items-center">
                    {file.media_type === 'video' ? (
                      <VideoCameraIcon className="h-8 w-8 text-blue-500 mr-3" />
                    ) : (
                      <MusicalNoteIcon className="h-8 w-8 text-green-500 mr-3" />
                    )}
                    <div className="flex-1">
                      <h4 className="text-sm font-medium text-gray-900">
                        {file.original_filename}
                      </h4>
                      <p className="text-sm text-gray-500">
                        {file.media_type === 'video' ? '视频' : '音频'}
                        {file.duration && ` • ${Math.round(file.duration)}秒`}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8">
              <VideoCameraIcon className="mx-auto h-12 w-12 text-gray-400" />
              <h3 className="mt-2 text-sm font-medium text-gray-900">暂无媒体文件</h3>
              <p className="mt-1 text-sm text-gray-500">
                上传视频或音频文件开始标注。
              </p>
            </div>
          )}
        </div>
      </div>

      {/* 标签列表 */}
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
            标签配置
          </h3>
          {labels.length > 0 ? (
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {labels.map((label) => (
                <div
                  key={label.id}
                  className="flex items-center p-3 border border-gray-200 rounded-lg"
                >
                  <div
                    className="w-4 h-4 rounded-full mr-3"
                    style={{ backgroundColor: label.color }}
                  ></div>
                  <span className="text-sm font-medium text-gray-900">
                    {label.name}
                  </span>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8">
              <TagIcon className="mx-auto h-12 w-12 text-gray-400" />
              <h3 className="mt-2 text-sm font-medium text-gray-900">暂无标签</h3>
              <p className="mt-1 text-sm text-gray-500">
                为项目配置标注标签。
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default ProjectDetail;