# Investigating Tradeoffs in Real-World Video Super-Resolution

## OSS

-

## TAGs

#CVPR #Y2022 #video_super_resolution

## Contributions

- We place an image cleaning module prior to propagation for removing degradations in the input images.
    - The phenomenon (long-term information) leads to a tradeoff between enhancing details and suppressing artifacts, since the synthesizing power of a network comes at the cost of amplifying noises and artifacts.
    - We further develop a dynamic refinement scheme that repeatedly applied the cleaning module to remove excessive degradations in the inputs.
- We propose a stochastic degradation scheme that effectively reduces the I/O bottleneck without sacrificing the output quality.
- We conclude that networks trained with longer sequence lengths rather than larger batches could more effectively employ the long-term information in the input sequence, improving stability. (with a fixed computational budget)
- We propose VideoLQ, a real-world video dataset consisting of diverse LR videos to cover various contents, resolutions, and degradations.


## Resources

- [ARXIV: the paper](https://arxiv.org/abs/2111.12704)
- [CVF: the paper](https://openaccess.thecvf.com/content/CVPR2022/papers/Chan_Investigating_Tradeoffs_in_Real-World_Video_Super-Resolution_CVPR_2022_paper.pdf)
- [GitHub: Official Repository: RealBasicVSR](https://github.com/ckkelvinchan/RealBasicVSR)
