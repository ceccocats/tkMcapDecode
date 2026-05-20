import sys
import numpy as np
import matplotlib.pyplot as plt

from mcap_protobuf.decoder import DecoderFactory
from mcap.reader import make_reader
from cloud import protoCloudToNumpy

def getImage(img_proto):
    # JPEG
    if img_proto.type == 10:
        # Convert the bytes into a NumPy uint8 array
        nparr = np.frombuffer(img_proto.data, np.uint8)

        # Decode the array into an image (OpenCV format)
        import cv2
        img = None
        if img_proto.channels == 3 or img_proto.channels == 4:
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        elif img_proto.channels == 1:
            img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
        else:
            raise TypeError("Unsupported channels: ", img_proto.channels)
        return img
    # uint8
    elif img_proto.type == 0:
        nparr = np.frombuffer(img_proto.data, np.uint8)
        img = nparr.reshape(img_proto.height, img_proto.width, img_proto.channels)
        return img
    # Float32
    elif img_proto.type == 3:
        nparr = np.frombuffer(img_proto.data, np.float32)
        img = nparr.reshape(img_proto.height, img_proto.width, img_proto.channels)
        return img
    else:
        raise TypeError("Unsupported image type: ", img_proto.type)


def decodeImage(proto_msg):
    print("image: ", proto_msg.width, "x", proto_msg.height, "type: ", proto_msg.type)
    img = getImage(proto_msg)
    print(np.shape(img))

    plt.figure(channel.topic)
    plt.cla()
    plt.imshow(img)
    plt.axis('off')
    plt.show(block=False)
    plt.pause(0.01)


def decodeGridmap(data):
    print(
        "gridmap: res: ",
        proto_msg.resolution,
        " dim: ",
        proto_msg.dimension[0],
        proto_msg.dimension[1],
    )
    img = getImage(proto_msg.image)
    print(np.shape(img))

    img_extent = [-proto_msg.dimension[0]/2, proto_msg.dimension[0]/2, -proto_msg.dimension[1]/2, proto_msg.dimension[1]/2]

    plt.figure(channel.topic)
    plt.cla()
    plt.imshow(img, extent=img_extent)
    plt.show(block=False)
    plt.pause(0.01)

def decodeCloud(data):
    points = protoCloudToNumpy(data)
    print("Pointcloud: ", np.shape(points))

    # debug viz
    import open3d as o3d
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points[:, :3])
    o3d.visualization.draw_geometries([pcd])

if __name__ == "__main__":
    img = None
    with open(sys.argv[1], "rb") as f:
        reader = make_reader(f, decoder_factories=[DecoderFactory()])
        for schema, channel, message, proto_msg in reader.iter_decoded_messages():
            print(f"msg {channel.topic} {schema.name} [{message.log_time}]")
            if schema.name == "proto.tk.msg.Image":
                decodeImage(proto_msg)
            if schema.name == "proto.tk.msg.GridMap":
                decodeGridmap(proto_msg)
            elif schema.name == "proto.tk.msg.Cloud":
                decodeCloud(proto_msg)
