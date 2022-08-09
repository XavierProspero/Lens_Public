from gicameramodel import CameraModel
import plotly.express as px
import argparse
import plotly.graph_objects as go


def main():
    parser = argparse.ArgumentParser(description='Arguments for camera model.')
    parser.add_argument('--R1', type=float, required="true",
                    help='Radius of lens on subject side in mm.')
    parser.add_argument('--R2', type=float, required="true",
                    help='Radius of lens on sensor side in mm.')
    parser.add_argument('--T', type=float, required="true",
                    help='Thickness of the lens at the center in mm.')
    parser.add_argument('--OD', type=float, required="true",
                    help='Aperture size of the lense in mm.')
    parser.add_argument('--D2', type=float, required="true",
                    help='Distance from back of lens to sensor in mm.')
    parser.add_argument('--D', type=float, required="true",
                    help='Distance from front of lense to object in mm.')
    parser.add_argument('--h', type=float, required="true",
                    help='Height of sensor in mm')
    parser.add_argument('--M', type=int, required="true",
                    help='Number of pixels in a row on sensor')
    parser.add_argument('--N', type=int, required="true",
                    help='Number of rays to shoot from point source')

    args = parser.parse_args()

    camera_model = CameraModel(args.R1, args.R2, args.T, args.OD, args.D2, args.h, args.M, args.D)
    camera_model.sample_point_source(args.N)

    # Make tthe image gray scale and get rid of coordinates.
    fig = px.imshow(camera_model.sensor.sensor, binary_string=True)
    fig.update_layout(coloraxis_showscale=False)
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)

    # Display helpful text.
    lines = [
        "R1:{},".format(args.R1),
        "R2:{},".format(args.R2),
        "T:{},".format(args.T),
        "OD:{},".format(args.OD),
        "D2:{},".format(args.D2),
        "D:{},".format(args.D),
        "h:{},".format(args.h),
        "M:{}.".format(args.D),
        "N:{}".format(args.N)
    ]
    dsplayText = '\n'.join(lines)

    fig.add_annotation(
        x=.5,
        y=0,
        text=dsplayText,
        xref="paper",
        yref="paper",
        showarrow=False,
        font_size=20, font_color='red')

    fig.show()



if __name__ == "__main__":
    main()
