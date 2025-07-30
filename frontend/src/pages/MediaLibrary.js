import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchMediaFiles, uploadMediaFile, deleteMediaFile } from '../store/slices/mediaSlice';
import { fetchProjects } from '../store/slices/projectsSlice';
import {
  VideoCameraIcon,
  MusicalNoteIcon,
  PlusIcon,
  TrashIcon,
  PlayIcon,
} from '@heroicons/react/24/outline';

function MediaLibrary() {
  const dispatch = useDispatch();
  const { mediaFiles, loading, error } = useSelector((state) => state.media);
  const { projects } = useSelector((state) => state.projects);
  const [selectedProject, setSelectedProject] = useState('');
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);

  useEffect(() => {
    dispatch(fetchMediaFiles());
    dispatch(fetchProjects());
  }, [dispatch]);

  const handleFileUpload = async (e) => {
    e.preventDefault();
    if (selectedFile && selectedProject) {
      await dispatch(uploadMediaFile({ file: selectedFile, projectId: selectedProject }));
      setShowUploadModal(false);
      setSelectedFile(null);
      setSelectedProject('');
    }
  };

  const handleDeleteFile = async (id) => {
    if (window.confirm('确定要删除这个文件吗？')) {
      await dispatch(deleteMediaFile(id));
    }
  };

  const filteredFiles = selectedProject
    ? mediaFiles.filter(file => file.project_id === parseInt(selectedProject))
    : mediaFiles;

  return (
    <div>
      <div className="mb-8 flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-semibold text-gray-900">媒体库</h1>
          <p className="mt-2 text-sm text-gray-600">
            管理您的视频和音频文件，上传新文件或查看现有文件。
          </p>
        </div>
        <button
          onClick={() => setShowUploadModal(true)}
          className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
        >
          <PlusIcon className="h-5 w-5 mr-2" />
          上传文件
        </button>
      </div>

      {/* 过滤器 */}
      <div className="mb-6">
        <select
          value={selectedProject}
          onChange={(e) => setSelectedProject(e.target.value)}
          className="px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
        >
          <option value="">所有项目</option>
          {projects.map((project) => (
            <option key={project.id} value={project.id}>
              {project.name}
            </option>
          ))}
        </select>
      </div>

      {error && (
        <div className="mb-4 bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded">
          {error}
        </div>
      )}

      {loading ? (
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          {filteredFiles.map((file) => (
            <div
              key={file.id}
              className="bg-white overflow-hidden shadow rounded-lg hover:shadow-md transition-shadow"
            >
              <div className="p-4">
                <div className="flex items-center mb-3">
                  {file.media_type === 'video' ? (
                    <VideoCameraIcon className="h-8 w-8 text-blue-500 mr-3" />
                  ) : (
                    <MusicalNoteIcon className="h-8 w-8 text-green-500 mr-3" />
                  )}
                  <div className="flex-1">
                    <h3 className="text-sm font-medium text-gray-900 truncate">
                      {file.original_filename}
                    </h3>
                    <p className="text-xs text-gray-500">
                      {file.media_type === 'video' ? '视频' : '音频'}
                      {file.duration && ` • ${Math.round(file.duration)}秒`}
                    </p>
                  </div>
                </div>

                <div className="flex items-center justify-between">
                  <span className="text-xs text-gray-500">
                    {Math.round(file.file_size / 1024 / 1024)}MB
                  </span>
                  <div className="flex space-x-2">
                    <button
                      onClick={() => handleDeleteFile(file.id)}
                      className="text-red-600 hover:text-red-800"
                    >
                      <TrashIcon className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {filteredFiles.length === 0 && !loading && (
        <div className="text-center py-12">
          <VideoCameraIcon className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900">暂无媒体文件</h3>
          <p className="mt-1 text-sm text-gray-500">
            上传视频或音频文件开始标注。
          </p>
          <div className="mt-6">
            <button
              onClick={() => setShowUploadModal(true)}
              className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
            >
              <PlusIcon className="h-5 w-5 mr-2" />
              上传文件
            </button>
          </div>
        </div>
      )}

      {/* 上传模态框 */}
      {showUploadModal && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
            <div className="mt-3">
              <h3 className="text-lg font-medium text-gray-900 mb-4">
                上传媒体文件
              </h3>
              <form onSubmit={handleFileUpload}>
                <div className="mb-4">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    选择项目
                  </label>
                  <select
                    required
                    value={selectedProject}
                    onChange={(e) => setSelectedProject(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  >
                    <option value="">请选择项目</option>
                    {projects.map((project) => (
                      <option key={project.id} value={project.id}>
                        {project.name}
                      </option>
                    ))}
                  </select>
                </div>
                <div className="mb-4">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    选择文件
                  </label>
                  <input
                    type="file"
                    required
                    accept="video/*,audio/*"
                    onChange={(e) => setSelectedFile(e.target.files[0])}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
                <div className="flex justify-end space-x-3">
                  <button
                    type="button"
                    onClick={() => setShowUploadModal(false)}
                    className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 border border-gray-300 rounded-md hover:bg-gray-200"
                  >
                    取消
                  </button>
                  <button
                    type="submit"
                    className="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700"
                  >
                    上传
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default MediaLibrary;