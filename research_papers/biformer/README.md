# BiFormer: Learning Bilateral Motion Estimation via Bilateral Transformer for 4K Video Frame Interpolation

## OSS

Proposed a model to do 4K video frame interpolation with Transformer.

## TAGs

#CVPR #Y2023 #video_frame_interpolation

## Methods

![](./assets/architecture.png)

First, we estimate global motion fields at a coarse scale via BiFormer. Second, we refine these global motion fields into final motion fields at a fine scale, by employing a motion up-sampler recurrently.

### BiFormer

![](./assets/biformer.png)
![](./assets/bcaa_1.png)
![](./assets/bcaa_2.png)

- BCA-A (Bilateral Cross Attention without Anchor)
    - In the beginning, $`\mathcal{F}_{0.5}`$ (the anchor) does not exist.
    - Use a feature from $`\mathcal{F}_{0}`$ as $`Q`$ and a feature from $`\mathcal{F}_{1}`$ as $`K`$. If they got lots of attention, there may be a pixel moving from $`Q`$ to $`K`$. NOTE: $`Q`$ and  $`K`$ are at point symmetric positions.
    - Use the attention to build the initial anchor (an initial guess of $`F_{0.5}`$).
- BCA+A (Bilateral Cross Attention with Anchor)
    - Now we have anchor, use $`F_{0.5}`$ as $`Q`$.
    - Use a feature from $`\mathcal{F}_{0}`$ as $`K_0`$ and a feature from $`\mathcal{F}_{1}`$ as $`K_1`$. If they got lots of attention, there may be a pixel moving from $`K_0`$ to $`K_1`$. NOTE: $`K_0`$ and  $`K_1`$ are at point symmetric positions.
    - Use the attention to fine tune the $`F_{0.5}`$.

### Local Motion Refinement: Upsampler

Transformer demands a huge number of parameters to process high-resolution input, so use CNN to upscale the motion fields.

![](./assets/bbcv.png)

BBCVs (Bilateral Block-wise Cost Volumes)

- Works like BCA+A (point symmetric).
- Provides information for upscaling.
- 👨🏼‍🦲 I do not know why 2x2 BBCV are not totally symmetric though.
- Cost volume: For each pixel, compute its cost of not similar to its neighbors in a window. For a HxWxC feature map, this yields HxWxSxS cost volumes while "S" is the window size.
    - $`C(p, \text{v}) = 1 - (F^1_p)^T F^2_{p + \text{v}}`$
    - $`\text{v}`$ is the motion. If both features are normalized and the same, then the cost is 0.

## Resources

- [ARXIV: The paper](https://arxiv.org/abs/2304.02225)
- [GitHub: Official implementation](https://github.com/JunHeum/BiFormer)
