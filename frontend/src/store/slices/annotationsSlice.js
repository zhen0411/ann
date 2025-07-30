import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { annotationsAPI } from '../../services/api';

// 异步thunk
export const fetchAnnotations = createAsyncThunk(
  'annotations/fetchAnnotations',
  async (params, { rejectWithValue }) => {
    try {
      const response = await annotationsAPI.getAnnotations(params);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || '获取标注列表失败');
    }
  }
);

export const createAnnotation = createAsyncThunk(
  'annotations/createAnnotation',
  async (annotationData, { rejectWithValue }) => {
    try {
      const response = await annotationsAPI.createAnnotation(annotationData);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || '创建标注失败');
    }
  }
);

export const updateAnnotation = createAsyncThunk(
  'annotations/updateAnnotation',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      const response = await annotationsAPI.updateAnnotation(id, data);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || '更新标注失败');
    }
  }
);

export const deleteAnnotation = createAsyncThunk(
  'annotations/deleteAnnotation',
  async (id, { rejectWithValue }) => {
    try {
      await annotationsAPI.deleteAnnotation(id);
      return id;
    } catch (error) {
      return rejectWithValue(error.response?.data || '删除标注失败');
    }
  }
);

export const reviewAnnotation = createAsyncThunk(
  'annotations/reviewAnnotation',
  async ({ id, status, comment }, { rejectWithValue }) => {
    try {
      const response = await annotationsAPI.reviewAnnotation(id, status, comment);
      return { id, status, comment };
    } catch (error) {
      return rejectWithValue(error.response?.data || '审阅标注失败');
    }
  }
);

const initialState = {
  annotations: [],
  currentAnnotation: null,
  loading: false,
  error: null,
};

const annotationsSlice = createSlice({
  name: 'annotations',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    setCurrentAnnotation: (state, action) => {
      state.currentAnnotation = action.payload;
    },
    clearCurrentAnnotation: (state) => {
      state.currentAnnotation = null;
    },
    addAnnotation: (state, action) => {
      state.annotations.push(action.payload);
    },
    updateAnnotationLocal: (state, action) => {
      const index = state.annotations.findIndex(a => a.id === action.payload.id);
      if (index !== -1) {
        state.annotations[index] = action.payload;
      }
    },
    removeAnnotation: (state, action) => {
      state.annotations = state.annotations.filter(a => a.id !== action.payload);
    },
  },
  extraReducers: (builder) => {
    builder
      // fetchAnnotations
      .addCase(fetchAnnotations.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchAnnotations.fulfilled, (state, action) => {
        state.loading = false;
        state.annotations = action.payload;
      })
      .addCase(fetchAnnotations.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      // createAnnotation
      .addCase(createAnnotation.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(createAnnotation.fulfilled, (state, action) => {
        state.loading = false;
        state.annotations.push(action.payload);
      })
      .addCase(createAnnotation.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      // updateAnnotation
      .addCase(updateAnnotation.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(updateAnnotation.fulfilled, (state, action) => {
        state.loading = false;
        const index = state.annotations.findIndex(a => a.id === action.payload.id);
        if (index !== -1) {
          state.annotations[index] = action.payload;
        }
        if (state.currentAnnotation?.id === action.payload.id) {
          state.currentAnnotation = action.payload;
        }
      })
      .addCase(updateAnnotation.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      // deleteAnnotation
      .addCase(deleteAnnotation.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(deleteAnnotation.fulfilled, (state, action) => {
        state.loading = false;
        state.annotations = state.annotations.filter(a => a.id !== action.payload);
        if (state.currentAnnotation?.id === action.payload) {
          state.currentAnnotation = null;
        }
      })
      .addCase(deleteAnnotation.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      // reviewAnnotation
      .addCase(reviewAnnotation.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(reviewAnnotation.fulfilled, (state, action) => {
        state.loading = false;
        const index = state.annotations.findIndex(a => a.id === action.payload.id);
        if (index !== -1) {
          state.annotations[index].status = action.payload.status;
          state.annotations[index].review_comment = action.payload.comment;
        }
      })
      .addCase(reviewAnnotation.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  },
});

export const {
  clearError,
  setCurrentAnnotation,
  clearCurrentAnnotation,
  addAnnotation,
  updateAnnotationLocal,
  removeAnnotation,
} = annotationsSlice.actions;

export default annotationsSlice.reducer;