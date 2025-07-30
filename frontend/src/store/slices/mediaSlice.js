import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { mediaAPI } from '../../services/api';

// 异步thunk
export const fetchMediaFiles = createAsyncThunk(
  'media/fetchMediaFiles',
  async (params, { rejectWithValue }) => {
    try {
      const response = await mediaAPI.getMediaFiles(params);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || '获取媒体文件列表失败');
    }
  }
);

export const uploadMediaFile = createAsyncThunk(
  'media/uploadMediaFile',
  async ({ file, projectId }, { rejectWithValue }) => {
    try {
      const response = await mediaAPI.uploadMediaFile(file, projectId);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || '上传文件失败');
    }
  }
);

export const deleteMediaFile = createAsyncThunk(
  'media/deleteMediaFile',
  async (id, { rejectWithValue }) => {
    try {
      await mediaAPI.deleteMediaFile(id);
      return id;
    } catch (error) {
      return rejectWithValue(error.response?.data || '删除文件失败');
    }
  }
);

const initialState = {
  mediaFiles: [],
  currentMediaFile: null,
  loading: false,
  error: null,
  uploadProgress: 0,
};

const mediaSlice = createSlice({
  name: 'media',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    setCurrentMediaFile: (state, action) => {
      state.currentMediaFile = action.payload;
    },
    clearCurrentMediaFile: (state) => {
      state.currentMediaFile = null;
    },
    setUploadProgress: (state, action) => {
      state.uploadProgress = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      // fetchMediaFiles
      .addCase(fetchMediaFiles.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchMediaFiles.fulfilled, (state, action) => {
        state.loading = false;
        state.mediaFiles = action.payload;
      })
      .addCase(fetchMediaFiles.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      // uploadMediaFile
      .addCase(uploadMediaFile.pending, (state) => {
        state.loading = true;
        state.error = null;
        state.uploadProgress = 0;
      })
      .addCase(uploadMediaFile.fulfilled, (state, action) => {
        state.loading = false;
        state.mediaFiles.push(action.payload);
        state.uploadProgress = 100;
      })
      .addCase(uploadMediaFile.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
        state.uploadProgress = 0;
      })
      // deleteMediaFile
      .addCase(deleteMediaFile.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(deleteMediaFile.fulfilled, (state, action) => {
        state.loading = false;
        state.mediaFiles = state.mediaFiles.filter(m => m.id !== action.payload);
        if (state.currentMediaFile?.id === action.payload) {
          state.currentMediaFile = null;
        }
      })
      .addCase(deleteMediaFile.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  },
});

export const { clearError, setCurrentMediaFile, clearCurrentMediaFile, setUploadProgress } = mediaSlice.actions;

export default mediaSlice.reducer;