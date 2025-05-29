import toast from 'react-hot-toast';
import styles from './ToastManager.module.css';

const ToastManager = {
  success: (message) => {
    toast.success(message);
  },

  error: (message) => {
    toast.error(message);
  },

  loading: (message) => {
    return toast.loading(message);
  },

  dismiss: (toastId) => {
    toast.dismiss(toastId);
  },

  customConfirm: (message, onConfirm, onCancel) => {
    toast((t) => (
      <div className={styles.toastContainer}>
        <p className={styles.toastMessage}>{message}</p>
        <div className={styles.toastButtons}>
          <button
            className={`${styles.toastButton} ${styles.confirmButton}`}
            onClick={() => {
              onConfirm();
              toast.dismiss(t.id);
            }}
          >
            Sim
          </button>
          <button
            className={`${styles.toastButton} ${styles.cancelButton}`}
            onClick={() => {
              if (onCancel) onCancel();
              toast.dismiss(t.id);
            }}
          >
            Não
          </button>
        </div>
      </div>
    ), {
      duration: Infinity,
    });
  },

  customConfirmAsync: (message, onConfirmAsync, onCancel) => {
    toast((t) => (
      <div className={styles.toastContainer}>
        <p className={styles.toastMessage}>{message}</p>
        <div className={styles.toastButtons}>
          <button
            className={`${styles.toastButton} ${styles.confirmButton}`}
            onClick={async () => {
              try {
                await onConfirmAsync();
              } catch (error) {
                toast.error('Erro ao processar a operação.');
              } finally {
                toast.dismiss(t.id);
              }
            }}
          >
            Sim
          </button>
          <button
            className={`${styles.toastButton} ${styles.cancelButton}`}
            onClick={() => {
              if (onCancel) onCancel();
              toast.dismiss(t.id);
            }}
          >
            Não
          </button>
        </div>
      </div>
    ), {
      duration: Infinity,
    });
  }
};

export default ToastManager;
