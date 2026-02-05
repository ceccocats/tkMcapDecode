import sys
import numpy as np
from mcap_protobuf.decoder import DecoderFactory
from mcap.reader import make_reader
from cloud import protoCloudToNumpy


def decodeImage(data):
    print("image: ", proto_msg.width, "x", proto_msg.height, "type: ", proto_msg.type) 
    # JPEG
    if(proto_msg.type == 10):
        # Convert the bytes into a NumPy uint8 array
        nparr = np.frombuffer(proto_msg.data, np.uint8)
        
        # Decode the array into an image (OpenCV format)
        import cv2
        img = None
        if proto_msg.channels == 3 or proto_msg.channels == 4:
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        elif proto_msg.channels == 1:
            img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
        else:
            raise TypeError("Unsupported channels: ", proto_msg.channels)

        # debug viz
        # cv2.imshow(channel.topic, img)
        # cv2.waitKey(1)   
    else:
        raise TypeError("Unsupported image type: ", proto_msg.type)

def decodeCloud(data):
    points = protoCloudToNumpy(data)
    print("Pointcloud: ", np.shape(points))

    # debug viz
    # import open3d as o3d
    # pcd = o3d.geometry.PointCloud()
    # pcd.points = o3d.utility.Vector3dVector(points[:, :3])
    # o3d.visualization.draw_geometries([pcd])

if __name__ == "__main__":
    img = None
    with open(sys.argv[1], "rb") as f:
        reader = make_reader(f, decoder_factories=[DecoderFactory()])
        for schema, channel, message, proto_msg in reader.iter_decoded_messages():
            print(f"msg {channel.topic} {schema.name} [{message.log_time}]")
            if(schema.name == "proto.tk.msg.Image"):
                decodeImage(proto_msg)
            elif(schema.name == "proto.tk.msg.Cloud"):
                decodeCloud(proto_msg)
