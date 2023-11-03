# NTIRE 2019 Challenge on Video Super-Resolution: Methods and Results

## OSS

Summarized 2 video super resolution challenges and proposed models.

## TAGs

#CVPRW #Y2019 #video_super_resolution

## Methods

The existing datasets (YT10, Va14, SPMCS, CDVL) have significant shortcomings
- They lack a standard training set
- Small test sets and resolution
- Mixed downsampling methods that are not standardized

### Track 1: Clean

We generate each LR frame from the HR REDS frame by using MATLAB function **imresize** with bucubic interpolation and downscaling factor 4.

### Track 2: Blur

All the videos used to create the REDS dataset are manually recorded with GoPro HERO6 Black. They were originally recorded in 1920x1080 resolution at 120 fps. ... Then the frames are interpolated using "Video frame interpolation via adaptive separable convolution" to virtually increase the frame rate up to 1920 fps so that averaged frames could exhibit smooth and realistic blurs without step artifacts.

## Resources

- [CVF: the paper](https://openaccess.thecvf.com/content_CVPRW_2019/papers/NTIRE/Nah_NTIRE_2019_Challenge_on_Video_Super-Resolution_Methods_and_Results_CVPRW_2019_paper.pdf)
