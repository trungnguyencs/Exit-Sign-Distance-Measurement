import json, cv2
import numpy as np
from matplotlib import pyplot as plt
from pnp import Point, Quadrilateral
import conf 

class Processing(object):
  def create_quadrilateral_arr(self, data, json_flag):
    """
    Create an array of quadrilateral objects from the input data json object
    """
    quadrilateral_arr = []
    if json_flag == 'from labelbox':
      for i in range(len(data)):
        id = data[i]['External ID']
        try:
          pts = data[i]['Label'][conf.LABEL][0]['geometry']
          p1 = Point(int(pts[0]['x']), int(pts[0]['y']))
          p2 = Point(int(pts[1]['x']), int(pts[1]['y']))
          p3 = Point(int(pts[2]['x']), int(pts[2]['y']))
          p4 = Point(int(pts[3]['x']), int(pts[3]['y']))
          quadrilateral_arr.append(Quadrilateral(id, (p1, p2, p3, p4)))
        except:
          continue
      quadrilateral_arr.sort(key=lambda x : x.id, reverse = False)

    elif json_flag == 'from reading imgs':
      for i in range(len(data)):
        id = data[i]['img_id']
        pts = data[i]['vertices_2D']
        p1 = Point(pts[0][0], pts[0][1])
        p2 = Point(pts[1][0], pts[1][1])
        p3 = Point(pts[2][0], pts[2][1])
        p4 = Point(pts[3][0], pts[3][1])
        obj = Quadrilateral(id, (p1, p2, p3, p4))
        obj.real_distance = int(data[i]['img_id'][0])
        quadrilateral_arr.append(obj)

    return quadrilateral_arr

  def find_distance_error(self, quadrilateral_arr):
    """
    Calulate the average pixel differences in x and y directions between
    the labels and the projected images
    """
    err = [0]*10
    count = [0]*10
    for quadrilateral in quadrilateral_arr:
      err[quadrilateral.real_distance] += abs(quadrilateral.distance - quadrilateral.real_distance)
      count[quadrilateral.real_distance] += 1
    ave_err = [err[i]/count[i] for i in range(2,10)]
    err_percentage = [err[i]/count[i]/i for i in range(2,10)]

    print('Image count per distance:')
    print(count)
    print('Ave error per distance:')
    print(ave_err)
    print('Error percentage:')
    print(err_percentage)

  def find_ave_proj_error(self, quadrilateral_arr):
    """
    Calulate the average pixel differences in x and y directions between
    the labels and the projected images
    """
    err_x, err_y = 0, 0
    for quadrilateral in quadrilateral_arr:
      x_err, y_err = quadrilateral.find_projection_err(quadrilateral.vertices_2D)
      err_x += x_err
      err_y += y_err
    return (err_x/len(quadrilateral_arr), err_y/len(quadrilateral_arr))

  def display_image(self, quadrilateral):
    """
    Display the image, the exit sign label boundaries and the normal Oxyz at the center of the exit sign
    """
    img = cv2.imread(conf.IMG_PATH + quadrilateral.id)
    window_name = 'Image ' + quadrilateral.id + ', Distance: ' + str(quadrilateral.distance)

    projected_orthogonals = quadrilateral.project_2D(quadrilateral.R_vec, quadrilateral.T_vec,\
                                                     conf.DEFAULT_ORTHOGONALS_3D).tolist()
    # Draw the projected vertices
    img = cv2.polylines(img, np.int32([quadrilateral.vertices_2D]),  
                      isClosed=True, color=(0, 255, 255), thickness=3)

    # Draw the normal vector at the center of the quadrilateral
    start_point = tuple(projected_orthogonals[0])
    end_point = tuple(projected_orthogonals[1])
    img = cv2.arrowedLine(img, start_point, end_point,  
                      color=(255, 0, 0), thickness=3, tipLength=0.25)

    start_point = tuple(projected_orthogonals[0])
    end_point = tuple(projected_orthogonals[2])
    img = cv2.arrowedLine(img, start_point, end_point,  
                      color=(0, 0, 255), thickness=3, tipLength=0.25)

    start_point = tuple(projected_orthogonals[0])
    end_point = tuple(projected_orthogonals[3])
    img = cv2.arrowedLine(img, start_point, end_point,  
                      color=(255, 0, 255), thickness=3, tipLength=0.25)   

    # img = cv2.resize(img, (672, 504))
    # cv2.imshow(window_name, img)
    # cv2.waitKey(1000)
    # cv2.destroyWindow(window_name)
    img_name = conf.ARROW_IMG_PATH + 'arrow_' + str(quadrilateral.distance)[:4] + '_' + quadrilateral.id
    cv2.imwrite(img_name, img)    

  def write_to_json(self, arr, json_file_name):
    """
    Write the quadrilateral array to a json output file
    """
    with open(json_file_name, "w") as outfile: 
      json_obj = json.dumps(arr, default=lambda x: x.__dict__, indent=4, sort_keys=True)
      outfile.write(json_obj)

def main():
  with open(conf.JSON_INPUT) as f:
    data = json.load(f)
  P = Processing()
  quadrilateral_arr = P.create_quadrilateral_arr(data, conf.JSON_FLAG)
  # P.write_to_json(quadrilateral_arr, conf.JSON_OUTPUT)

  print('***********************************************************************')
  ave_x_err, ave_y_err = P.find_ave_proj_error(quadrilateral_arr)
  print('Average x-axis projection error: ' + str(ave_x_err))
  print('Average y-axis projection error: ' + str(ave_y_err))

  print('***********************************************************************')
  for i in range(len(quadrilateral_arr)):
    # i = np.random.randint(0, len(quadrilateral_arr))
    quadrilateral = quadrilateral_arr[i]
    print(quadrilateral.id + ' ' + str(quadrilateral.distance))
    # img = P.display_image(quadrilateral)

  print('***********************************************************************')
  print(len(quadrilateral_arr))
  print('***********************************************************************')
  if conf.model == 'groundtruth_1920x1440_iPhone8':
    P.find_distance_error(quadrilateral_arr)
  
if __name__== "__main__":
  main()


