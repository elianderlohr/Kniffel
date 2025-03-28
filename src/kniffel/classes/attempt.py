from src.kniffel.classes.status import KniffelStatus
from src.kniffel.classes.options import KniffelOptions
from src.kniffel.classes.dice_set import DiceSet
from src.kniffel.classes.kniffel_check import KniffelCheck
from src.kniffel.classes.kniffel_option import KniffelOptionClass
import src.kniffel.classes.custom_exceptions as ex


class Attempt:
    attempts = []
    status = KniffelStatus.INIT
    option = KniffelOptions.DEFAULT
    logging = False
    selected_option: KniffelOptionClass = None  # type: ignore

    def __init__(self, logging: bool = False):
        self.attempts = []
        self.logging = logging

    def get_attempt(self, index: int) -> DiceSet:
        """
        Get attempts
        """
        return self.attempts[index]

    def get_selected_option(self) -> KniffelOptionClass:
        """
        Get selected option
        """
        return self.selected_option

    def is_active(self):
        """
        Is active attempt or finished attempt
        """
        if self.count() > 3:
            return False
        elif self.status.value == KniffelStatus.FINISHED.value:
            return False
        elif self.option.value is not KniffelOptions.DEFAULT.value:
            return False
        else:
            return True

    def count(self) -> int:
        """Get count of attempts

        :return: amount of attempts
        """
        return len(self.attempts)

    def attempts_left(self) -> int:
        """Return attempts left

        Returns:
            int: amount of turns left in int
        """
        return 3 - self.count()

    def add_attempt(self, keep: list = [], dice_set: DiceSet = None):  # type: ignore
        """
        Add new attempt.
        Optionally keep selected dices

        :param list keep: hot encoded array which dices to keep. (1 = keep, 0 = re-roll)
        :param DiceSet dice_set: dice set to use for the attempt
        """
        self.status = KniffelStatus.ATTEMPTING

        if dice_set is None:
            dice_set = DiceSet()
            # assert sorted(dice_set.to_int_list()) == dice_set.to_int_list()

        if self.count() >= 3:
            raise ex.TurnFinishedException()
        else:
            if self.is_active() and self.count() > 0 and keep is not None:
                old_set = self.get_latest()

                for i in range(1, len(keep) + 1):
                    if keep[i - 1] == 1:
                        dice_set.set_dice(index=i, dice=old_set.get_dice(i))

            self.attempts.append(dice_set)

    def finish_attempt(self, option: KniffelOptions) -> KniffelOptionClass:
        """
        Finish attempt

        :param KniffelOptions option: selected option how to finish the attempt
        """
        if self.is_active():
            self.status = KniffelStatus.FINISHED
            self.option = option

            if option.value == KniffelOptions.ONES.value:
                self.selected_option = KniffelCheck().check_1(self.attempts[-1])
            elif option.value == KniffelOptions.TWOS.value:
                self.selected_option = KniffelCheck().check_2(self.attempts[-1])
            elif option.value == KniffelOptions.THREES.value:
                self.selected_option = KniffelCheck().check_3(self.attempts[-1])
            elif option.value == KniffelOptions.FOURS.value:
                self.selected_option = KniffelCheck().check_4(self.attempts[-1])
            elif option.value == KniffelOptions.FIVES.value:
                self.selected_option = KniffelCheck().check_5(self.attempts[-1])
            elif option.value == KniffelOptions.SIXES.value:
                self.selected_option = KniffelCheck().check_6(self.attempts[-1])

            elif option.value == KniffelOptions.THREE_TIMES.value:
                self.selected_option = KniffelCheck().check_three_times(
                    self.attempts[-1]
                )
            elif option.value == KniffelOptions.FOUR_TIMES.value:
                self.selected_option = KniffelCheck().check_four_times(
                    self.attempts[-1]
                )
            elif option.value == KniffelOptions.FULL_HOUSE.value:
                self.selected_option = KniffelCheck().check_full_house(
                    self.attempts[-1]
                )
            elif option.value == KniffelOptions.SMALL_STREET.value:
                self.selected_option = KniffelCheck().check_small_street(
                    self.attempts[-1]
                )
            elif option.value == KniffelOptions.LARGE_STREET.value:
                self.selected_option = KniffelCheck().check_large_street(
                    self.attempts[-1]
                )
            elif option.value == KniffelOptions.KNIFFEL.value:
                self.selected_option = KniffelCheck().check_kniffel(self.attempts[-1])
            elif option.value == KniffelOptions.CHANCE.value:
                self.selected_option = KniffelCheck().check_chance(self.attempts[-1])

            elif option.value == KniffelOptions.ONES_SLASH.value:
                possibility = KniffelCheck().check_1(self.attempts[-1])

                self.selected_option = KniffelOptionClass(
                    "ones_slash",
                    0,
                    ds=None,  # type: ignore
                    id=KniffelOptions.ONES_SLASH,
                    is_possible=True,
                )
            elif option.value == KniffelOptions.TWOS_SLASH.value:
                possibility = KniffelCheck().check_2(self.attempts[-1])

                self.selected_option = KniffelOptionClass(
                    "twos_slash",
                    0,
                    ds=None,  # type: ignore
                    id=KniffelOptions.TWOS_SLASH,
                    is_possible=True,
                )
            elif option.value == KniffelOptions.THREES_SLASH.value:
                possibility = KniffelCheck().check_3(self.attempts[-1])

                self.selected_option = KniffelOptionClass(
                    "threes_slash",
                    0,
                    ds=None,  # type: ignore
                    id=KniffelOptions.THREES_SLASH,
                    is_possible=True,
                )
            elif option.value == KniffelOptions.FOURS_SLASH.value:
                possibility = KniffelCheck().check_4(self.attempts[-1])

                self.selected_option = KniffelOptionClass(
                    "fours_slash",
                    0,
                    ds=None,  # type: ignore
                    id=KniffelOptions.FOURS_SLASH,
                    is_possible=True,
                )
            elif option.value == KniffelOptions.FIVES_SLASH.value:
                possibility = KniffelCheck().check_5(self.attempts[-1])

                self.selected_option = KniffelOptionClass(
                    "fives_slash",
                    0,
                    ds=None,  # type: ignore
                    id=KniffelOptions.FIVES_SLASH,
                    is_possible=True,
                )
            elif option.value == KniffelOptions.SIXES_SLASH.value:
                possibility = KniffelCheck().check_6(self.attempts[-1])

                self.selected_option = KniffelOptionClass(
                    "sixes_slash",
                    0,
                    ds=None,  # type: ignore
                    id=KniffelOptions.SIXES_SLASH,
                    is_possible=True,
                )

            elif option.value == KniffelOptions.THREE_TIMES_SLASH.value:
                possibility = KniffelCheck().check_three_times(self.attempts[-1])

                self.selected_option = KniffelOptionClass(
                    "three_times_slash",
                    0,
                    ds=None,  # type: ignore
                    id=KniffelOptions.THREE_TIMES_SLASH,
                    is_possible=True,
                )
            elif option.value == KniffelOptions.FOUR_TIMES_SLASH.value:
                possibility = KniffelCheck().check_four_times(self.attempts[-1])

                self.selected_option = KniffelOptionClass(
                    "four_times_slash",
                    0,
                    ds=None,  # type: ignore
                    id=KniffelOptions.FOUR_TIMES_SLASH,
                    is_possible=True,
                )
            elif option.value == KniffelOptions.FULL_HOUSE_SLASH.value:
                possibility = KniffelCheck().check_full_house(self.attempts[-1])

                self.selected_option = KniffelOptionClass(
                    "full_house_slash",
                    0,
                    ds=None,  # type: ignore
                    id=KniffelOptions.FULL_HOUSE_SLASH,
                    is_possible=True,
                )
            elif option.value == KniffelOptions.SMALL_STREET_SLASH.value:
                possibility = KniffelCheck().check_small_street(self.attempts[-1])

                self.selected_option = KniffelOptionClass(
                    "small_street_slash",
                    0,
                    ds=None,  # type: ignore
                    id=KniffelOptions.SMALL_STREET_SLASH,
                    is_possible=True,
                )
            elif option.value == KniffelOptions.LARGE_STREET_SLASH.value:
                possibility = KniffelCheck().check_large_street(self.attempts[-1])

                self.selected_option = KniffelOptionClass(
                    "large_street_slash",
                    0,
                    ds=None,  # type: ignore
                    id=KniffelOptions.LARGE_STREET_SLASH,
                    is_possible=True,
                )
            elif option.value == KniffelOptions.KNIFFEL_SLASH.value:
                possibility = KniffelCheck().check_kniffel(self.attempts[-1])

                self.selected_option = KniffelOptionClass(
                    "kniffel_slash",
                    0,
                    ds=None,  # type: ignore
                    id=KniffelOptions.KNIFFEL_SLASH,
                    is_possible=True,
                )
            elif option.value == KniffelOptions.CHANCE_SLASH.value:
                possibility = KniffelCheck().check_chance(self.attempts[-1])

                self.selected_option = KniffelOptionClass(
                    "chance_slash",
                    0,
                    ds=None,  # type: ignore
                    id=KniffelOptions.CHANCE_SLASH,
                    is_possible=True,
                )

        return self.selected_option

    def get_latest(self) -> DiceSet:
        """
        Get latest attempt
        """
        return self.attempts[-1]

    def mock(self, mock: DiceSet):
        """
        Mock set of dices instead of random throws

        :param DiceSet mock: set of dices
        """
        self.add_attempt(dice_set=mock)

    def to_int_list(self):
        """
        Transform list of dice objects to simple int array list
        """
        return [v.to_int_list() for v in self.attempts]

    def print(self):
        """
        Print attempts
        """
        if self.status.value == KniffelStatus.FINISHED.value:
            print(
                "Turn (finished): "
                + str(len(self.attempts))
                + " - "
                + str(self.to_int_list())
                + " - "
                + str(self.selected_option)
            )
        else:
            print("Turn: " + str(len(self.attempts)) + " - " + str(self.to_int_list()))
