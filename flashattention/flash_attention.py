import numpy as np
import time
import psutil
import os


class AttentionSimulator:
    def __init__(self, seq_length: int, head_dim: int):
        self.seq_length = seq_length
        self.head_dim = head_dim

    def standard_attention(
        self, Q: np.ndarray, K: np.ndarray, V: np.ndarray
    ) -> np.ndarray:
        """Simulate standard attention with full memory allocation
        Args:
            Q: Query matrix shape (seq_length, head_dim)
            K: Key matrix shape (seq_length, head_dim)
            V: Value matrix shape (seq_length, head_dim)
        Returns:
            output: Attention output shape (seq_length, head_dim)
        """
        # Compute full attention matrix
        attention_scores = np.matmul(Q, K.transpose(-1, -2))
        attention_scores = attention_scores / np.sqrt(self.head_dim)

        # Softmax
        attention_probs = np.exp(attention_scores) / np.sum(
            np.exp(attention_scores), axis=-1, keepdims=True
        )

        # Compute output
        output = np.matmul(attention_probs, V)
        return output

    def flash_attention(
        self, Q: np.ndarray, K: np.ndarray, V: np.ndarray, block_size: int = 1024
    ) -> np.ndarray:
        """Simulate FlashAttention with blocked computation"""
        output = np.zeros_like(Q)
        normalizer = np.zeros((self.seq_length, 1))

        # Process in blocks to simulate tiling
        for i in range(0, self.seq_length, block_size):
            i_end = min(i + block_size, self.seq_length)
            Q_block = Q[i:i_end]

            # Initialize block accumulators
            block_output = np.zeros_like(Q_block)
            block_normalizer = np.zeros((i_end - i, 1))

            for j in range(0, self.seq_length, block_size):
                j_end = min(j + block_size, self.seq_length)
                K_block = K[j:j_end]
                V_block = V[j:j_end]

                # Compute attention scores for this block
                scores = np.matmul(Q_block, K_block.transpose(-1, -2))
                scores = scores / np.sqrt(self.head_dim)

                # Compute local softmax
                exp_scores = np.exp(scores)
                block_normalizer += np.sum(exp_scores, axis=-1, keepdims=True)
                block_output += np.matmul(exp_scores, V_block)

            # Store results for this block
            output[i:i_end] = block_output
            normalizer[i:i_end] = block_normalizer

        # Final normalization
        output = output / normalizer
        return output


def benchmark_attention(seq_length: int, head_dim: int):
    """Benchmark both attention implementations"""
    # Initialize random inputs
    Q = np.random.randn(seq_length, head_dim)
    K = np.random.randn(seq_length, head_dim)
    V = np.random.randn(seq_length, head_dim)
    print(Q.shape, K.shape, V.shape)
    simulator = AttentionSimulator(seq_length, head_dim)

    # Benchmark standard attention
    start_time = time.time()
    start_memory = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024  # MB

    standard_output = simulator.standard_attention(Q, K, V)

    standard_time = time.time() - start_time
    standard_memory = (
        psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024 - start_memory
    )

    # Benchmark flash attention
    start_time = time.time()
    start_memory = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024

    flash_output = simulator.flash_attention(Q, K, V)

    flash_time = time.time() - start_time
    flash_memory = (
        psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024 - start_memory
    )

    return {
        "standard_time": standard_time,
        "flash_time": flash_time,
        "standard_memory": standard_memory,
        "flash_memory": flash_memory,
        "output_diff": np.mean(np.abs(standard_output - flash_output)),
    }


# Run benchmark with different sequence lengths
sequence_lengths = [1000, 2000, 4000]
head_dim = 64

for seq_len in sequence_lengths:
    print(f"\nBenchmarking with sequence length: {seq_len}")
    results = benchmark_attention(seq_len, head_dim)
    print(f"Standard Attention Time: {results['standard_time']:.4f}s")
    print(f"Flash Attention Time: {results['flash_time']:.4f}s")
    print(f"Standard Attention Memory: {results['standard_memory']:.2f}MB")
    print(f"Flash Attention Memory: {results['flash_memory']:.2f}MB")
    print(f"Output Difference: {results['output_diff']:.8f}")
