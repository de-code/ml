import behaviors
import unittest

class TestTargetFollowingBehavior(unittest.TestCase):

#  *  {-45}-------{ 0 }-------{45}
#  *      | +-----[ +y]-----+ | 
#  *      | |               | | 
#  *      | |               | | 
#  *  {-90} [-x]  [0,0]  [+x] {90}
#  *      | |               | | 
#  *      | |               | | 
#  *      | +-----[ -y]-----+ |
#  * {-135}-------{180}-------{135}
 
    def setUp(self):
        self.small_angle = 5.0
        self.large_angle = 50.0

    def test_calculate_motor_speeds_no_correction_facing_north(self):
        behavior = behaviors.TargetFollowingBehavior()
        behavior.set_target_coordinates_list([[0.0, 0.0]])
        sensorData = {
            'coordinates': [0.0, 1000.0],
            'compass_heading': 0.0}
        speeds = behavior.calculate_motor_speeds(sensorData)
        self.assertGreater(speeds[0], 0.0, "speeds[0]")
        self.assertEqual(round(speeds[0], 5), round(speeds[1], 5), "speeds[0] == speeds[1]")

    def test_calculate_motor_speeds_should_slightly_correct_to_the_right_facing_north(self):
        behavior = behaviors.TargetFollowingBehavior()
        behavior.set_target_coordinates_list([[0.0, 0.0]])
        sensorData = {
            'coordinates': [0.0, 1000.0],
            'compass_heading': -self.small_angle}
        speeds = behavior.calculate_motor_speeds(sensorData)
        self.assertGreater(speeds[1], 0.0, "speeds[1]")
        self.assertGreater(speeds[0], speeds[1], "speeds[0] > speeds[1]")

    def test_calculate_motor_speeds_should_slightly_correct_to_the_left_facing_north(self):
        behavior = behaviors.TargetFollowingBehavior()
        behavior.set_target_coordinates_list([[0.0, 0.0]])
        sensorData = {
            'coordinates': [0.0, 1000.0],
            'compass_heading': self.small_angle}
        speeds = behavior.calculate_motor_speeds(sensorData)
        self.assertGreater(speeds[0], 0.0, "speeds[1]")
        self.assertGreater(speeds[1], speeds[0], "speeds[0] < speeds[1]")

    def test_calculate_motor_speeds_should_strongly_correct_to_the_right_facing_north(self):
        behavior = behaviors.TargetFollowingBehavior()
        behavior.set_target_coordinates_list([[0.0, 0.0]])
        sensorData = {
            'coordinates': [0.0, 1000.0],
            'compass_heading': -self.large_angle}
        speeds = behavior.calculate_motor_speeds(sensorData)
        self.assertGreater(speeds[0], 0.0, "speeds[0]")
        self.assertEqual(round(speeds[0], 5), round(-speeds[1], 5), "speeds[0] == -speeds[1]")

    def test_calculate_motor_speeds_should_strongly_correct_to_the_right_facing_left(self):
        behavior = behaviors.TargetFollowingBehavior()
        behavior.set_target_coordinates_list([[0.0, 0.0]])
        sensorData = {
            'coordinates': [0.0, 1000.0],
            'compass_heading': self.large_angle}
        speeds = behavior.calculate_motor_speeds(sensorData)
        self.assertGreater(speeds[1], 0.0, "speeds[1]")
        self.assertEqual(round(speeds[0], 5), round(-speeds[1], 5), "speeds[0] == -speeds[1]")

    def test_calculate_motor_speeds_no_correction_facing_south(self):
        behavior = behaviors.TargetFollowingBehavior()
        behavior.set_target_coordinates_list([[0.0, 0.0]])
        sensorData = {
            'coordinates': [0.0, -1000.0],
            'compass_heading': 180.0}
        speeds = behavior.calculate_motor_speeds(sensorData)
        self.assertGreater(speeds[0], 0.0, "speeds[0]")
        self.assertEqual(round(speeds[0], 5), round(speeds[1], 5), "speeds[0] == speeds[1]")

    def test_calculate_motor_speeds_should_slightly_correct_to_the_right_facing_south(self):
        behavior = behaviors.TargetFollowingBehavior()
        behavior.set_target_coordinates_list([[0.0, 0.0]])
        sensorData = {
            'coordinates': [0.0, -1000.0],
            'compass_heading': 180.0 - self.small_angle}
        speeds = behavior.calculate_motor_speeds(sensorData)
        self.assertGreater(speeds[1], 0.0, "speeds[1]")
        self.assertGreater(speeds[0], speeds[1], "speeds[0] > speeds[1]")

    def test_calculate_motor_speeds_should_slightly_correct_to_the_left_facing_south(self):
        behavior = behaviors.TargetFollowingBehavior()
        behavior.set_target_coordinates_list([[0.0, 0.0]])
        sensorData = {
            'coordinates': [0.0, -1000.0],
            'compass_heading': 180.0 + self.small_angle}
        speeds = behavior.calculate_motor_speeds(sensorData)
        self.assertGreater(speeds[0], 0.0, "speeds[1]")
        self.assertGreater(speeds[1], speeds[0], "speeds[0] < speeds[1]")
        
    def test_calculate_motor_speeds_no_correction_facing_east(self):
        behavior = behaviors.TargetFollowingBehavior()
        behavior.set_target_coordinates_list([[0.0, 0.0]])
        sensorData = {
            'coordinates': [-1000.0, 0.0],
            'compass_heading': 90.0}
        speeds = behavior.calculate_motor_speeds(sensorData)
        self.assertGreater(speeds[0], 0.0, "speeds[0]")
        self.assertEqual(round(speeds[0], 5), round(speeds[1], 5), "speeds[0] == speeds[1]")

    def test_calculate_motor_speeds_should_slightly_correct_to_the_right_facing_east(self):
        behavior = behaviors.TargetFollowingBehavior()
        behavior.set_target_coordinates_list([[0.0, 0.0]])
        sensorData = {
            'coordinates': [-1000.0, 0.0],
            'compass_heading': 90.0 - self.small_angle}
        speeds = behavior.calculate_motor_speeds(sensorData)
        self.assertGreater(speeds[1], 0.0, "speeds[1]")
        self.assertGreater(speeds[0], speeds[1], "speeds[0] > speeds[1]")

    def test_calculate_motor_speeds_should_slightly_correct_to_the_left_facing_east(self):
        behavior = behaviors.TargetFollowingBehavior()
        behavior.set_target_coordinates_list([[0.0, 0.0]])
        sensorData = {
            'coordinates': [-1000.0, 0.0],
            'compass_heading': 90.0 + self.small_angle}
        speeds = behavior.calculate_motor_speeds(sensorData)
        self.assertGreater(speeds[0], 0.0, "speeds[1]")
        self.assertGreater(speeds[1], speeds[0], "speeds[0] < speeds[1]")

    def test_calculate_motor_speeds_should_return_zero_speeds_and_done_should_return_true_when_target_reached_exactly(self):
        behavior = behaviors.TargetFollowingBehavior()
        behavior.set_target_coordinates_list([[0.0, 0.0]])
        sensorData = {
            'coordinates': [0.0, 0.0],
            'compass_heading': 0.0}
        speeds = behavior.calculate_motor_speeds(sensorData)
        self.assertEquals(speeds[0], 0.0, "speeds[0]")
        self.assertEquals(speeds[1], 0.0, "speeds[1]")
        self.assertEquals(behavior.done(), True, "done")


if __name__ == '__main__':
    unittest.main()