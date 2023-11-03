# Quadratic Video Interpolation

## OSS

Proposed a network to interpolate video frames with acceleration distance formula.

## TAGs

#NeurIPS #Y2019 #video_frame_interpolation

## Methods

![](./assets/pipeline_color2.png)

- We use **PWC-Net: CNNs for Optical Flow Using Pyramid, Warping and Cost Volume** to estimate flows.
- Quadratic flow prediction
    - $`f_{0 \to t} = \int_0^t [ v_0 + \int_0^k a_{\tau} d\tau] dk`$
        - $`f_{0 \to t}`$ : the displacement of the pixel from fram 0 to t
        - $`v_0`$ : the velocity at frame 0
        - $`a_\tau`$ : the acceleration at frame $`\tau`$
    - $`f_{0 \to t} = \frac{ f_{0 \to 1} + f_{0 \to -1} }{2} \times t^2 + \frac{ f_{0 \to 1} - f_{0 \to -1} }{2} \times t`$
        - $`f_{0 \to 1} + f_{0 \to -1}`$
            - the acceleration
        - $`f_{0 \to 1} - f_{0 \to -1}`$
            - the velocity ( Note, $`f_{ 0 \to 1 }`$ and $`f_{ 0 \to -1}`$ are in **opposite** directions)
- Flow reversal layer
    - $`f_{ t \to 0 }(u) = \frac{ \sum_{x + f_{0 \to t}(x) \in \mathcal{N}(u)} w (|| x + f_{0 \to t}(x) - u ||_2) (-f_{0 \to t}(x)) }{ \sum_{x + f_{0 \to t}(x) \in \mathcal{N}(u)} w (|| x + f_{0 \to t}(x) - u ||_2) }`$
        - $`\sum_{x + f_{0 \to t}(x) \in \mathcal{N}(u)} w (|| x + f_{0 \to t}(x) - u ||_2) (-f_{0 \to t}(x))`$
        - $`\sum_{x + f_{0 \to t}(x) \in \mathcal{N}(u)} w (|| x + f_{0 \to t}(x) - u ||_2)`$
        - $`\mathcal{N}(u)`$ : neighborhood of pixel __u__
        - $`w(d) = e^{ -d^2 / \sigma^2 }`$ : gaussian weight
        - The proposed flow reversal layer is conceptually similar to the surface splatting in computer graphics where the optical flow in our work is replaced by camera projection (❓).
        - During training, while the reversal layer itself does not have learnable parameters, it is differentiable and allows the gradients to be back-propagated to the flow estimation module and thus enables end-to-end training of the whole system.
- Frame synthesis
    - Adaptive flow filtering.
        - Inspired by the median filter which samples only one pixel from a neighborhood and avoids the issues of weighted averaging, we propose a flow filtering network to adaptively sample the flow map for removing outliers.
        - $`f_{t \to 0}^\prime (u) = f_{ t \to 0 } (u + \delta(u)) + r(u)`$
            - $`f_{t \to 0}^\prime (u)`$ : filtered backward flow
            - $`\delta(u)`$ : learned sampling offset
            - $`r(u)`$ : residual map
    - Warping and fusing source frames
        - $`\hat{I}_t(u) = \frac{ (1 - t) m(u) I_0 (u + f_{t \to 0}^\prime(u)) + t(1 - m(u))I_1(u + f_{t \to 1}^\prime(u)) }{ (1 - t) m(u) + t (1 - m(u)) }`$
            - $`(1 - t) m(u) I_0 (u + f_{t \to 0}^\prime(u)) + t(1 - m(u))I_1(u + f_{t \to 1}^\prime(u))`$
            - $`(1 - t) m(u) + t (1 - m(u))`$
            - $`m`$ : learned mask
- $`\mathcal{L} = || \hat{I}_t - I_t ||_1 + \lambda || \phi (\hat{I}_t) - \phi(I_t) ||_2`$
    - reconstruction loss and perceptual loss


## Resources

- [ARXIV: The paper](https://arxiv.org/abs/1911.00627)
- [NeurIPS: The paper](https://proceedings.neurips.cc/paper_files/paper/2019/file/d045c59a90d7587d8d671b5f5aec4e7c-Paper.pdf)
- [Project page](https://sites.google.com/view/xiangyuxu/qvi_nips19)
- [Official implementation](https://www.google.com/url?q=https%3A%2F%2Fwww.dropbox.com%2Fs%2F07kykjaw55pbwra%2Fnips19_qvi_eval_release.zip%3Fdl%3D0&sa=D&sntz=1&usg=AOvVaw2E7LkvphHUNXYL9hTbKnwO)
- [YouTube - Demo Video](https://youtu.be/vemHEbkWMAI)
